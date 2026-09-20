# Signet7 Outlook add-in

Read: passive check. Unsigned mail stays quiet.

Write in Outlook. This pane is not a composer. Seal outgoing mail with
**Sign and send email**. That step attaches `Signet7-sealed.eml`. The
sender token is saved on this mailbox after the first paste. Ordinary
Send is not sealed. Auto-seal, if they opt in, is the localhost SMTP
helper on named desks only. That hop seals the letter itself. Table:
https://signet7.io/docs#seal-where See https://signet7.io/smtp.html

Sideload `manifest.xml`. Open https://aka.ms/olksideload → My add-ins →
Add a custom add-in → Add from File. The new Apps store cannot upload
XML. Not AppSource. IT pushes this add-in from Microsoft 365 admin →
Settings → Integrated apps. Do not push Signet7 desktop to every laptop.
Steps: https://signet7.io/docs#entra-push
Not Exchange. Recipients are not required to install.

Hosted files: https://signet7.io/outlook/taskpane.html and compose.html
Recipient check API: https://verify.signet7.io
Sender seal API: https://seal.signet7.io
