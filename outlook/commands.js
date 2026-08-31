/* global Office */
Office.onReady(function () {});

function onMessageReadHandler(event) {
  if (Office.context && Office.context.mailbox && Office.context.mailbox.item && Office.context.mailbox.item.notificationMessages) {
    Office.context.mailbox.item.notificationMessages.replaceAsync(
      "signet7Passive",
      {
        type: Office.MailboxEnums.ItemNotificationMessageType.InformationalMessage,
        message: "Signet7 is checking this sealed message in the background.",
        persistent: false,
        icon: "Icon16"
      }
    );
  }
  if (event && event.completed) event.completed();
}

function onMessageSendHandler(event) {
  if (event && event.completed) event.completed({ allowEvent: true });
}

if (typeof Office !== "undefined" && Office.actions && Office.actions.associate) {
  Office.actions.associate("onMessageReadHandler", onMessageReadHandler);
  Office.actions.associate("onMessageSendHandler", onMessageSendHandler);
  Office.actions.associate("onMessageRead", onMessageReadHandler);
}
