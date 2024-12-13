# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import user_pb2 as user__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in user_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class UserCommandServiceStub(object):
    """Servizio per i comandi (modifiche dello stato)
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterUser = channel.unary_unary(
                '/user.UserCommandService/RegisterUser',
                request_serializer=user__pb2.RegisterUserRequest.SerializeToString,
                response_deserializer=user__pb2.CommandResponse.FromString,
                _registered_method=True)
        self.UpdateUser = channel.unary_unary(
                '/user.UserCommandService/UpdateUser',
                request_serializer=user__pb2.UpdateUserRequest.SerializeToString,
                response_deserializer=user__pb2.CommandResponse.FromString,
                _registered_method=True)
        self.DeleteUser = channel.unary_unary(
                '/user.UserCommandService/DeleteUser',
                request_serializer=user__pb2.DeleteUserRequest.SerializeToString,
                response_deserializer=user__pb2.CommandResponse.FromString,
                _registered_method=True)
        self.UpdateThreshold = channel.unary_unary(
                '/user.UserCommandService/UpdateThreshold',
                request_serializer=user__pb2.UpdateThresholdRequest.SerializeToString,
                response_deserializer=user__pb2.CommandResponse.FromString,
                _registered_method=True)
        self.RemoveThreshold = channel.unary_unary(
                '/user.UserCommandService/RemoveThreshold',
                request_serializer=user__pb2.RemoveThresholdRequest.SerializeToString,
                response_deserializer=user__pb2.CommandResponse.FromString,
                _registered_method=True)


class UserCommandServiceServicer(object):
    """Servizio per i comandi (modifiche dello stato)
    """

    def RegisterUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateThreshold(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveThreshold(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserCommandServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterUser': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterUser,
                    request_deserializer=user__pb2.RegisterUserRequest.FromString,
                    response_serializer=user__pb2.CommandResponse.SerializeToString,
            ),
            'UpdateUser': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateUser,
                    request_deserializer=user__pb2.UpdateUserRequest.FromString,
                    response_serializer=user__pb2.CommandResponse.SerializeToString,
            ),
            'DeleteUser': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUser,
                    request_deserializer=user__pb2.DeleteUserRequest.FromString,
                    response_serializer=user__pb2.CommandResponse.SerializeToString,
            ),
            'UpdateThreshold': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateThreshold,
                    request_deserializer=user__pb2.UpdateThresholdRequest.FromString,
                    response_serializer=user__pb2.CommandResponse.SerializeToString,
            ),
            'RemoveThreshold': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveThreshold,
                    request_deserializer=user__pb2.RemoveThresholdRequest.FromString,
                    response_serializer=user__pb2.CommandResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'user.UserCommandService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('user.UserCommandService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class UserCommandService(object):
    """Servizio per i comandi (modifiche dello stato)
    """

    @staticmethod
    def RegisterUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserCommandService/RegisterUser',
            user__pb2.RegisterUserRequest.SerializeToString,
            user__pb2.CommandResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserCommandService/UpdateUser',
            user__pb2.UpdateUserRequest.SerializeToString,
            user__pb2.CommandResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserCommandService/DeleteUser',
            user__pb2.DeleteUserRequest.SerializeToString,
            user__pb2.CommandResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateThreshold(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserCommandService/UpdateThreshold',
            user__pb2.UpdateThresholdRequest.SerializeToString,
            user__pb2.CommandResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RemoveThreshold(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserCommandService/RemoveThreshold',
            user__pb2.RemoveThresholdRequest.SerializeToString,
            user__pb2.CommandResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class UserQueryServiceStub(object):
    """Servizio per le query (recupero dati)
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllData = channel.unary_unary(
                '/user.UserQueryService/GetAllData',
                request_serializer=user__pb2.Empty.SerializeToString,
                response_deserializer=user__pb2.AllDataResponse.FromString,
                _registered_method=True)
        self.GetLastStockValue = channel.unary_unary(
                '/user.UserQueryService/GetLastStockValue',
                request_serializer=user__pb2.EmailRequest.SerializeToString,
                response_deserializer=user__pb2.StockValueResponse.FromString,
                _registered_method=True)
        self.GetAverageStockValue = channel.unary_unary(
                '/user.UserQueryService/GetAverageStockValue',
                request_serializer=user__pb2.AverageStockRequest.SerializeToString,
                response_deserializer=user__pb2.StockValueResponse.FromString,
                _registered_method=True)


class UserQueryServiceServicer(object):
    """Servizio per le query (recupero dati)
    """

    def GetAllData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLastStockValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAverageStockValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserQueryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllData,
                    request_deserializer=user__pb2.Empty.FromString,
                    response_serializer=user__pb2.AllDataResponse.SerializeToString,
            ),
            'GetLastStockValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLastStockValue,
                    request_deserializer=user__pb2.EmailRequest.FromString,
                    response_serializer=user__pb2.StockValueResponse.SerializeToString,
            ),
            'GetAverageStockValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAverageStockValue,
                    request_deserializer=user__pb2.AverageStockRequest.FromString,
                    response_serializer=user__pb2.StockValueResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'user.UserQueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('user.UserQueryService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class UserQueryService(object):
    """Servizio per le query (recupero dati)
    """

    @staticmethod
    def GetAllData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserQueryService/GetAllData',
            user__pb2.Empty.SerializeToString,
            user__pb2.AllDataResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetLastStockValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserQueryService/GetLastStockValue',
            user__pb2.EmailRequest.SerializeToString,
            user__pb2.StockValueResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAverageStockValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/user.UserQueryService/GetAverageStockValue',
            user__pb2.AverageStockRequest.SerializeToString,
            user__pb2.StockValueResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
