# # import asyncio
# #
# from .celery_worker import celery
# #
# # from mongo.mongo_crud import content_crud
# #
# #
# # async def async_func(post_id):
# #     await content_crud.get_post(post_id)
# #
# #
# @celery.task(name='plus_task', queue='main-queue')
# def plus_task(a, b):
#     result = a + b
#     return result
#
# #
# # @celery.task(name='resizing_images', queue='main-queue')
# # def resizing(post_id):
# #     loop = asyncio.get_event_loop()
# #     coroutine = async_func(post_id)
# #     loop.run_until_complete(coroutine)
# #     print(coroutine)
