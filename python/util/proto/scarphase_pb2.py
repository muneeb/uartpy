# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='scarphase.proto',
  package='scarphase.proto',
  serialized_pb='\n\x0fscarphase.proto\x12\x0fscarphase.proto\"\x99\x01\n\x06Window\x12\x0b\n\x03pid\x18\x01 \x02(\x05\x12\x36\n\nprediction\x18\x02 \x01(\x0b\x32\".scarphase.proto.Window.Prediction\x12\x11\n\tsignature\x18\x03 \x03(\x02\x1a\x37\n\nPrediction\x12\x12\n\nprediction\x18\x01 \x02(\x05\x12\x15\n\nconfidence\x18\x02 \x01(\x05:\x01\x30')




_WINDOW_PREDICTION = descriptor.Descriptor(
  name='Prediction',
  full_name='scarphase.proto.Window.Prediction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='prediction', full_name='scarphase.proto.Window.Prediction.prediction', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='confidence', full_name='scarphase.proto.Window.Prediction.confidence', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=135,
  serialized_end=190,
)

_WINDOW = descriptor.Descriptor(
  name='Window',
  full_name='scarphase.proto.Window',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='pid', full_name='scarphase.proto.Window.pid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='prediction', full_name='scarphase.proto.Window.prediction', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='signature', full_name='scarphase.proto.Window.signature', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_WINDOW_PREDICTION, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=37,
  serialized_end=190,
)

_WINDOW_PREDICTION.containing_type = _WINDOW;
_WINDOW.fields_by_name['prediction'].message_type = _WINDOW_PREDICTION
DESCRIPTOR.message_types_by_name['Window'] = _WINDOW

class Window(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Prediction(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _WINDOW_PREDICTION
    
    # @@protoc_insertion_point(class_scope:scarphase.proto.Window.Prediction)
  DESCRIPTOR = _WINDOW
  
  # @@protoc_insertion_point(class_scope:scarphase.proto.Window)

# @@protoc_insertion_point(module_scope)
