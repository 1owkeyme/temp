import cqrs
import pytest

from tests.mock import mock_dependencies
from tests.mock import mock_di


@pytest.fixture
def mocked_request_mediator() -> cqrs.RequestMediator:
    return mock_dependencies.mock_request_mediator_factory(di_container=mock_di.di_container_factory())
