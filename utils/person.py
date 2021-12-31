from enum import Enum

from utils.profile import Profile


class Sex(Enum):
    MALE = 0
    FEMALE = 1


class Person:
    def __init__(
        self,
        series: int,
        name: str,
        sex: Sex,
        job: str,
        mobile: int,
        wechat: str,
        email: str,
        id: str,
        city: str,
        address: str,
        order_id_20: int,
        profile: Profile,
    ):
        self.series = series
        self.name = name
        self.sex = sex
        self.job = job
        self.mobile = mobile
        self.wechat = wechat
        self.email = email
        self.id = id
        self.city = city
        self.address = address
        self.order_id_20 = order_id_20
        self.profile = profile

    def __repr__(self) -> str:
        return (
            f"series={self.series}, name={self.name}, sex={self.sex}, "
            f"job={self.job}, mobile={self.mobile}, "
            f"wechat={self.wechat}, email={self.email}, id={self.id}, city={self.city}, "
            f"address={self.address}, order_id_20 = {self.order_id_20}, profile={self.profile}"
        )
