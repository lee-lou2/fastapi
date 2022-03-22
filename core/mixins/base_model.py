from abc import ABCMeta, abstractmethod


class BaseModelABC(metaclass=ABCMeta):
    def __init__(self):
        self.model = self.Meta.model

    @property
    def _fit_model_attr(self):
        """
        모델 속성 외 데이터 제거
        :return:
        """
        return {
            key: value
            for key, value in self.__dict__.items()
            if key in dir(self.model)
        }

    def _schema_to_model(self, **kwargs):
        """
        스키마를 모델로 변환
        :param kwargs:
        :return:
        """
        return self.model(**self._fit_model_attr, **kwargs)

    @abstractmethod
    class Meta:
        model = None


class BaseModelCreateMixin(BaseModelABC):
    def save(self, db=None, commit=False, **kwargs):
        """
        모델 생성
        :param kwargs:
        :param db:
        :param commit:
        :return:
        """
        obj = self._schema_to_model(**kwargs)
        if db is None:
            return obj
        # 데이터 저장
        db.add(obj)
        if commit:
            db.commit()
        return obj

    @classmethod
    def bulk_create(cls, db, **kwargs):
        """
        대량 등록
        :param kwargs:
        :param db:
        :return:
        """
        assert db is not None, 'Not Found Database Connection'
        objs = kwargs.pop('objs')
        for obj in objs:
            db.add(obj.save())
        db.commit()
        return True

    class Meta:
        pass


class BaseModelUpdateMixin(BaseModelABC):
    def update(self, obj_id: int, db, commit=False, **kwargs):
        """
        모델 업데이트
        :param kwargs:
        :param obj_id:
        :param db:
        :param commit:
        :return:
        """
        assert db is not None, 'Not Found Database Connection'
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        # Todo 업데이트 코드 작성 필요
        if commit:
            db.commit()
        return obj

    class Meta:
        pass


class BaseModelDeleteMixin(BaseModelABC):
    def destroy(self, obj_id: int, db, commit=False, **kwargs):
        """
        모델 삭제
        :param kwargs:
        :param obj_id:
        :param db:
        :param commit:
        :return:
        """
        assert db is not None, 'Not Found Database Connection'
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        db.delete(obj)
        if commit:
            db.commit()
        return obj

    class Meta:
        pass
