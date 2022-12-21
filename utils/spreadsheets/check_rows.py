from loguru import logger
from models.pushes import Push
from sqlalchemy import select
from sqlalchemy.orm import scoped_session


async def check_count_rows(session: scoped_session, lesson_type: str="test") -> int | None:
    """
        check_count_rows ...
    """
    
    count_query = f"SELECT COUNT(*) FROM payments WHERE lesson_type = '{lesson_type}'"
    count_exec = await session.execute(count_query)
    count_result = count_exec.fetchone()

    push_query = select(Push).where(Push.file==lesson_type)
    push_exec = await session.execute(push_query)
    push_result = push_exec.fetchone()

    if count_result[0] >= push_result[0].offset * push_result[0].limit:
        push_result = push_result[0]
        logger.info(f"PUSHING! ", lesson_type, push_result.offset+1)
        await Push.update_offset(session, lesson_type, push_result.offset+1)
        return (push_result.offset-1) * push_result.limit

    return
