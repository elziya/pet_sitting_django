import random
from datetime import timedelta
from random import randint

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from web.models import User, Pet, Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_date = now()
        user = User.objects.first()
        pets = Pet.objects.filter(user=user)

        posts = []

        for day_index in range(30):
            current_date -= timedelta(days=1)

            for post_index in range(randint(5, 10)):
                start_date = current_date + timedelta(days=randint(1, 10))
                end_date = start_date + timedelta(days=randint(1, 30))

                posts.append(Post(
                    title=f'generated {day_index}-{post_index}',
                    post_date=current_date,
                    start_date=start_date,
                    end_date=end_date,
                    content=f'generated content {day_index}-{post_index}',
                    opened=random.choice((True, False)),
                    price=randint(100, 3000),
                    user=user
                ))

        saved_posts = Post.objects.bulk_create(posts)
        post_pets = []
        for post in saved_posts:
            count_of_pets = randint(1, len(pets))
            for pet_index in range(count_of_pets):
                post_pets.append(
                    Post.pets.through(post_id=post.id, pet_id=pets[pet_index].id)
                )
        Post.pets.through.objects.bulk_create(post_pets)
