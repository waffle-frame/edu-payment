from models.pushes import Push
from sqlalchemy.orm import scoped_session


async def check_rows(db: scoped_session, file_name: str="test"):
    """
        check_count_rows ...
    """
    
    offset = await Push.get_offset(db, file_name)

    data, sheets = await Push.get_data_for_upload(db, offset, file_name)
    if data is None or sheets is None:
        return None, sheets

    if data == []:
        return None, sheets

    return data, sheets
