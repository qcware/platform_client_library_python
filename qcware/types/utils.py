from pydantic import ValidationError


def pydantic_model_abridge_validation_errors(
    model, max_num_errors: int, *args, **kwargs
):
    try:
        return model(*args, **kwargs)

    except ValidationError as error:
        # noinspection PyTypeChecker
        abridged_error = ValidationError(
            errors=error.raw_errors[:max_num_errors], model=model
        )
        raise abridged_error from None
