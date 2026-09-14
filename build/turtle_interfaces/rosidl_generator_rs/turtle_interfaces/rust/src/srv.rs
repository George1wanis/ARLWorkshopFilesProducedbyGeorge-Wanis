#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to turtle_interfaces__srv__ShapeCommand_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ShapeCommand_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub command: std::string::String,

}



impl Default for ShapeCommand_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ShapeCommand_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ShapeCommand_Request {
  type RmwMsg = super::srv::rmw::ShapeCommand_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        command: msg.command.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      command: msg.command.to_string(),
    }
  }
}


// Corresponds to turtle_interfaces__srv__ShapeCommand_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ShapeCommand_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for ShapeCommand_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ShapeCommand_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ShapeCommand_Response {
  type RmwMsg = super::srv::rmw::ShapeCommand_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "turtle_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__turtle_interfaces__srv__ShapeCommand() -> *const std::ffi::c_void;
}

// Corresponds to turtle_interfaces__srv__ShapeCommand
#[allow(missing_docs, non_camel_case_types)]
pub struct ShapeCommand;

impl rosidl_runtime_rs::Service for ShapeCommand {
    type Request = ShapeCommand_Request;
    type Response = ShapeCommand_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__turtle_interfaces__srv__ShapeCommand() }
    }
}


