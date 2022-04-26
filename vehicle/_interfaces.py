from typing import Tuple, TypeAlias, Union, Dict, Any, List

VoltageType: TypeAlias = Union[int, float, None]
IdType: TypeAlias = Union[str, int, None]
PinVoltageFormDataBodyType = Dict[str, Tuple[None, IdType]]
PinVoltageBodyByIdType = Dict[str, Any]
PinsVoltagesBodyByIdsType = Dict[str, List[PinVoltageBodyByIdType]]

SystemsType: TypeAlias = Union[object, None]
