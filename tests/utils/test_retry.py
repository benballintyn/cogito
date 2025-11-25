import pytest

from cogito.utils.retry import async_retry


@pytest.mark.asyncio
async def test_retry_success():
    @async_retry(max_retries=3)
    async def always_succeeds():
        return "Success!"

    result = await always_succeeds()
    assert result == "Success!"


@pytest.mark.asyncio
async def test_retry_failure():
    @async_retry(max_retries=3, exceptions=(ValueError,))
    async def always_fails():
        raise ValueError("Failure")

    with pytest.raises(ValueError, match="Failure"):
        await always_fails()


@pytest.mark.asyncio
async def test_retry_with_exponential_backoff():
    attempts = 0

    @async_retry(max_retries=3, backoff_factor=0.1, exceptions=(ValueError,))
    async def sometimes_fails():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Simulated failure")
        return "Recovered!"

    result = await sometimes_fails()
    assert result == "Recovered!"
    assert attempts == 3
