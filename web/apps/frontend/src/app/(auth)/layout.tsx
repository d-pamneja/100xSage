export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="m-auto flex h-full w-[440px] items-center justify-center px-4 md:px-0">
      {children}
    </div>
  );
}
