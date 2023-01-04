from pydantic import BaseModel, validator


class User(BaseModel):
    id: int
    username: str

    @validator("id")
    def check_id_that_less_then_two(cls, v):
        if v > 2:
            raise ValueError('Id is not less then two')
        else:
            return v
