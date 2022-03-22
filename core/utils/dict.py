class DepthOfDictionary:
    def __init__(self, _dict, default=None):
        """
        기본 설정
        :param _dict:
        :param default:
        """
        self.dict = _dict
        self.default = default

    def get_value(self, *args):
        # 속성 값 조회
        _dict = self.dict
        for i, arg in enumerate(args):
            _dict = _dict.get(arg, {} if len(args) != i + 1 else self.default)
        return _dict
