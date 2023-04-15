# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=isinstance-second-argument-not-valid-type
from typing import Any, Dict, List, Optional, Type

from flask_appbuilder.models.filters import BaseFilter
from flask_appbuilder.models.sqla import Model
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, class_mapper
from sqlalchemy import or_

from app.api.db_models import db
from app.api.dao.exceptions import (
    DAOConfigError,
    DAOCreateFailedError,
    DAODeleteFailedError,
    DAOUpdateFailedError,
)
import logging

log = logging.getLogger(__name__)


class BaseDAO:
    """
    Base DAO, implement base CRUD sqlalchemy operations
    """

    model_cls: Optional[Type[Model]] = None
    """
    Child classes need to state the Model class so they don't need to implement basic
    create, update and delete methods
    """
    base_filter: Optional[BaseFilter] = None
    """
    Child classes can register base filtering to be applied to all filter methods
    """

    @classmethod
    def kwarg_or_filter(cls, session=None, limit=1000, cursor=0, **find_by_kwargs):
        """
        :param session: Pass in session to make concurrent querires in 1 request
        :param limit: Pass in limit
        :param cursor: Pass in cursor
        :param find_by_kwargs: keys with list values to search by in
        :return: list of ORMs
        """
        session = session or db.session
        not_null_filters = []
        query = session.query(cls.model_cls)
        for kwarg_key, kwarg_val in find_by_kwargs.items():
            filter = cls.model_cls.__getattribute__(cls.model_cls, kwarg_key).in_(
                kwarg_val
            )
            not_null_filters.append(filter)
        if len(not_null_filters) > 0:
            query = query.filter(or_(*not_null_filters))
        return query.limit(limit).offset(cursor).all()

    @classmethod
    def kwarg_filter(cls, session=None, limit=100, cursor=0, **find_by_kwargs):
        """
        Filter on a model by kwargs
        """
        session = session or db.session
        query = session.query(cls.model_cls)

        for kwarg_key, kwarg_val in find_by_kwargs.items():
            query = query.filter(
                cls.model_cls.__getattribute__(cls.model_cls, kwarg_key).in_(kwarg_val)
            )

        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, session)
            query = cls.base_filter("id", data_model).apply(
                query, None
            )  # pylint: disable=not-callable

        return query.limit(limit).offset(cursor).all()

    @classmethod
    def find_by_id(cls, model_id: int, session: Session = None) -> Model:
        """
        Find a model by id, if defined applies `base_filter`
        """
        session = session or db.session
        query = session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, session)
            query = cls.base_filter("id", data_model).apply(
                query, None
            )  # pylint: disable=not-callable
        return query.filter_by(id=model_id).one_or_none()

    @classmethod
    def find_by_ids(cls, model_ids: List[int], session: Session = None) -> List[Model]:
        """
        Find a List of models by a list of ids, if defined applies `base_filter`
        """
        session = session or db.session
        id_col = getattr(cls.model_cls, "id", None)
        if id_col is None:
            return []
        query = session.query(cls.model_cls).filter(id_col.in_(model_ids))
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter("id", data_model).apply(
                query, None
            )  # pylint: disable=not-callable
        return query.all()

    @classmethod
    def find_all(cls, session: Session = None) -> List[Model]:
        """
        Get all that fit the `base_filter`
        """
        session = session or db.session
        query = session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter("id", data_model).apply(
                query, None
            )  # pylint: disable=not-callable
        return query.all()

    @classmethod
    def find_one_or_none(
        cls, session: Session = None, **filter_by: Any
    ) -> Optional[Model]:
        """
        Get the first that fit the `base_filter`
        """
        session = session or db.session
        query = session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter("id", data_model).apply(
                query, None
            )  # pylint: disable=not-callable
        return query.filter_by(**filter_by).one_or_none()

    @classmethod
    def filter(cls, session: Session = None, **filter_by: Any) -> Optional[Model]:
        """
        Get the first that fit the `base_filter`
        """
        session = session or db.session
        query = session.query(cls.model_cls)
        if cls.base_filter:
            data_model = SQLAInterface(cls.model_cls, db.session)
            query = cls.base_filter("id", data_model).apply(
                query, None
            )  # pylint: disable=not-callable
        return query.filter_by(**filter_by).all()

    @classmethod
    def create(
        cls,
        properties: Dict[str, Any],
        commit: bool = True,
        session: Session = None,
    ) -> Model:
        """
        Generic for creating models
        :raises: DAOCreateFailedError
        """
        session = session or db.session
        if cls.model_cls is None:
            raise DAOConfigError()
        model = cls.model_cls()  # pylint: disable=not-callable
        for key, value in properties.items():
            setattr(model, key, value)
        try:
            session.add(model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            session.rollback()
            log.error(f"[baseDao.Create] Error Updating Model:{properties}, err={ex}")
            raise DAOCreateFailedError(exception=ex) from ex
        return model

    @classmethod
    def save(
        cls,
        instance_model: Model,
        commit: bool = True,
        session: Session = None,
    ) -> Model:
        """
        Generic for saving models
        :raises: DAOCreateFailedError
        """
        session = session or db.session
        if cls.model_cls is None:
            raise DAOConfigError()
        if not isinstance(instance_model, cls.model_cls):
            raise DAOCreateFailedError(
                "the instance model is not a type of the model class"
            )
        try:
            db.session.add(instance_model)
            if commit:
                db.session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            db.session.rollback()
            log.error(f"[baseDao.Save] Error Updating Model:{instance_model}, err={ex}")
            raise DAOCreateFailedError(exception=ex) from ex
        return instance_model

    @classmethod
    def update(
        cls,
        model: Model,
        properties: Dict[str, Any],
        commit: bool = True,
        session: Session = None,
    ) -> Model:
        """
        Generi c update a model
        :raises: DAOCreateFailedError
        """
        session = session or db.session
        for key, value in properties.items():
            setattr(model, key, value)
        try:
            session.merge(model)
            if commit:
                session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            session.rollback()
            log.error(f"Error Updating Model:{model}, err={ex}")
            raise DAOUpdateFailedError(exception=ex) from ex
        return model

    @classmethod
    def delete(
        cls, model: Model, commit: bool = True, session: Session = None
    ) -> Model:
        """
        Generic delete a model
        :raises: DAOCreateFailedError
        """
        try:
            session = session or db.session
            session.delete(model)
            if commit:
                session.commit()
        except SQLAlchemyError as ex:  # pragma: no cover
            session.rollback()
            log.error(f"Error Deleting Model:{model}, err={ex}")
            raise DAODeleteFailedError(exception=ex) from ex
        return model
