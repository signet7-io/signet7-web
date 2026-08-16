/* global Office */
Office.onReady(function () {});

function onMessageRead(event) {
  if (typeof Office !== "undefined" && Office.context && Office.context.mailbox && Office.context.mailbox.item) {
    Office.context.mailbox.item.notificationMessages.replaceAsync(
      "signet7Passive",
      {
        type: Office.MailboxEnums.ItemNotificationMessageType.InformationalMessage,
        message: "Signet7 is checking this message in the background.",
        persistent: false,
        icon: "Icon16",
      }
    );
  }
  if (event && event.completed) event.completed();
}

if (typeof Office !== "undefined" && Office.actions && Office.actions.associate) {
  Office.actions.associate("onMessageRead", onMessageRead);
}
