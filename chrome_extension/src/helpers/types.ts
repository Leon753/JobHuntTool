export type EmailPartBody = {
    data: String
    size: Number
}

export type EmailPart = {
    partId: String
    mimeType: String
    fileName: String
    headers: any
    body: EmailPartBody
}
