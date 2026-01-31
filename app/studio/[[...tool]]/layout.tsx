// app/studio/[[...tool]]/layout.tsx
export const metadata = {
  title: 'Admin | Fashion Website',
  description: 'Content management for Fashion Website',
}

export default function StudioLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  )
}
