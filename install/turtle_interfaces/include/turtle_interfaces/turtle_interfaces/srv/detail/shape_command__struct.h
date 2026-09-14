// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from turtle_interfaces:srv/ShapeCommand.idl
// generated code does not contain a copyright notice

#ifndef TURTLE_INTERFACES__SRV__DETAIL__SHAPE_COMMAND__STRUCT_H_
#define TURTLE_INTERFACES__SRV__DETAIL__SHAPE_COMMAND__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'command'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ShapeCommand in the package turtle_interfaces.
typedef struct turtle_interfaces__srv__ShapeCommand_Request
{
  rosidl_runtime_c__String command;
} turtle_interfaces__srv__ShapeCommand_Request;

// Struct for a sequence of turtle_interfaces__srv__ShapeCommand_Request.
typedef struct turtle_interfaces__srv__ShapeCommand_Request__Sequence
{
  turtle_interfaces__srv__ShapeCommand_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtle_interfaces__srv__ShapeCommand_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ShapeCommand in the package turtle_interfaces.
typedef struct turtle_interfaces__srv__ShapeCommand_Response
{
  bool success;
  rosidl_runtime_c__String message;
} turtle_interfaces__srv__ShapeCommand_Response;

// Struct for a sequence of turtle_interfaces__srv__ShapeCommand_Response.
typedef struct turtle_interfaces__srv__ShapeCommand_Response__Sequence
{
  turtle_interfaces__srv__ShapeCommand_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} turtle_interfaces__srv__ShapeCommand_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // TURTLE_INTERFACES__SRV__DETAIL__SHAPE_COMMAND__STRUCT_H_
