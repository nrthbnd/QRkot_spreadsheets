from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from sqlalchemy import func

from constants import (
    FORMAT, GOOGLE_SHEETS_OBG, GOOGLE_SHEETS_VERSION,
    PROP_TITLE, PROP_LOCALE, SHEET_TYPE, SHEET_ID,
    SHEET_TITLE, ROW_COUNT, COLUMN_COUNT, SPREADSHEET_ID,
    PERMISSION_TYPE, PERMISSION_ROLE,
    GOOGLE_DRIVE_OBJ, GOOGLE_DRIVE_VERSION, PERMISSION_FIELD,
    TABLE_VALUE_DESC, TABLE_VALUE_COL_1, TABLE_VALUE_COL_2, TABLE_VALUE_COL_3,
    MAJOR_DIMENSION, VALUES_RANGE, VALUE_INPUT_OPTION,
    NAME_LABEL, DESCRIPTION_LABEL, COLLECTION_TIME_LABEL,
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создать документ."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        GOOGLE_SHEETS_OBG,
        GOOGLE_SHEETS_VERSION
    )
    spreadsheet_body = {
        'properties': {'title': PROP_TITLE + now_date_time,
                       'locale': PROP_LOCALE},
        'sheets': [{'properties': {
            'sheetType': SHEET_TYPE,
            'sheetId': SHEET_ID,
            'title': SHEET_TITLE,
            'gridProperties': {
                'rowCount': ROW_COUNT,
                'columnCount': COLUMN_COUNT
            }
        }}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response[SPREADSHEET_ID]
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle,
) -> None:
    """Предоставить права доступа."""
    permissions_body = {
        'type': PERMISSION_TYPE,
        'role': PERMISSION_ROLE,
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover(
        GOOGLE_DRIVE_OBJ,
        GOOGLE_DRIVE_VERSION,
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields=PERMISSION_FIELD,
        )
    )


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list[dict],
        wrapper_services: Aiogoogle,
) -> None:
    """Обновить данные в google-таблице."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        GOOGLE_SHEETS_OBG,
        GOOGLE_SHEETS_VERSION,
    )

    table_values = [
        [PROP_TITLE, now_date_time],
        [TABLE_VALUE_DESC],
        [TABLE_VALUE_COL_1, TABLE_VALUE_COL_2, TABLE_VALUE_COL_3],
    ]

    for item in charity_projects:
        new_row = [
            item[NAME_LABEL],
            item[COLLECTION_TIME_LABEL],
            item[DESCRIPTION_LABEL],
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': MAJOR_DIMENSION,
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=VALUES_RANGE.format(len(table_values)),
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body,
        )
    )


async def calculate_collection_time(
        create_date: datetime,
        close_date: datetime,
):
    """Найти время, затраченное на сбор пожертвований для проекта."""
    return func.julianday(close_date) - (
        func.julianday(create_date))
