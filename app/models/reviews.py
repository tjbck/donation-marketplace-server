
from pydantic import BaseModel
from typing import List, Union
import time
import uuid
import config


DB = config.db

#####################
# Model
#####################


class ReviewModel(BaseModel):
    id: str
    user_id: str
    reviewer_id: str
    rating: int  # 1-5
    content: str
    createdAt: int = int(time.time())


#####################
# Table
#####################

class ReviewsTable:
    def __init__(self, db):
        self.db = db
        self.collection = db.reviews

    def insert_review(self, user_id: str, reviewer_id: str, rating: int, content: str) -> Union[None, ReviewModel]:
        review = ReviewModel(**{
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "reviewer_id": reviewer_id,
            "rating": rating,
            "content": content,
        })

        result = self.collection.insert_one(review.dict())
        return review if result.acknowledged else None

    def get_reviews_by_user_id(self, user_id: str) -> List[ReviewModel]:
        reviews = list(self.collection.find(
            {"user_id": user_id}, {"_id": False}).sort('_id', -1))
        return [ReviewModel(**review) for review in reviews]


Reviews = ReviewsTable(DB)
