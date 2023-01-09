from models.pushes import Push
from sqlalchemy.orm import scoped_session


async def check_rows(db: scoped_session, file_name: str="test"):
    """
        check_count_rows ...
    """
    
    offset = await Push.get_offset(db, file_name)

    data = await Push.get_data_for_upload(db, offset, file_name)
    if data is None or data == []:
        return None

    return data
