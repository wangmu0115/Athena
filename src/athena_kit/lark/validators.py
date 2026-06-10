from athena_kit.http import create_biz_code_validator

LARK_SUCCESS_VALIDATOR = create_biz_code_validator(
    code_key="code",
    success_codes=(0,),
    message_key="msg",
)
