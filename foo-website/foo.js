const CONVERSATION_ID = "conversationId"
const SUPPORT_AGENT_NAME = "Sam Smith"


function get_company_prompt() {
  const queryParams = $.param({ "company_domain": "udemy.com" })
  $.get({
    url: 'http://localhost:3000/customer/prompt?' + queryParams,
    success: function (response) {
      const data = response.data
      const content = data.prompt
      $("#chat-start").append(
        ChatBubbleForSupportComponent(SUPPORT_AGENT_NAME, content)
      )
      //TODO: poll messages
    },
    error: function (data) {
      console.log(data);
      alert("woops! couldn't connect to server");
    },
    timeout: 10000
  })
}

function send_msg(msgText) {
  $.post({
    url: 'http://localhost:3000/customer/send',
    data: {
      "company_domain": "udemy.com",
      "conversation_ref": localStorage.getItem(CONVERSATION_ID),
      "content": msgText
    },
    success: function (response) {
      console.log(response)
      const data = response.data;
      localStorage.setItem(CONVERSATION_ID, data.conversation_ref);

    },

  });
}

function ChatBubbleForSupportComponent(nameOfSupportAgent, msg) {
  function LeftItemComponent(context) {
    return $("<p/>").addClass("move-left").text(context)
  }
  const topComponent = $("<div/>").addClass("support-chat small p-2 ms-3 mb-3 rounded-3");
  return topComponent.append(LeftItemComponent(nameOfSupportAgent))
    .append(LeftItemComponent(msg))
}


function ChatBubbleForCustomerComponent(msg) {
  function RightItemComponent(context) {
    return $("<p/>").addClass("move-right").text(context)
  }
  const topComponent = $("<div/>").addClass("small p-2 ms-3 mb-3 rounded-3");
  console.log("customer here")
  return topComponent.append(RightItemComponent("You"))
    .append(RightItemComponent(msg))

}


function updateCustomerChat() {
  const messageContent = $("#chat-text").val();
  console.log(messageContent);
  $("#chat-start").append(
    ChatBubbleForCustomerComponent(messageContent)
  );
  $("#chat-text").val("") //clear input
  const conversationId = localStorage.getItem(CONVERSATION_ID);

  // TODO: send message to api
  send_msg(messageContent)
}



$(document).ready(() => {
  console.log("ready");

  get_company_prompt(); // or get conversation history

  $("#submit-chat").click(updateCustomerChat);
  $("#chat-text").keypress(function (event) {
    const keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13') {
      updateCustomerChat();
    }
  });
});