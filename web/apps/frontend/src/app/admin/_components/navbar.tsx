import NavbarRoutes from "./navbar-routes";
import { MobileSidebar } from "./mobile-sidebar";

const Navbar = async () => {
  return (
    <div className="flex h-full items-center border-b border-b-slate-800 p-2 shadow-sm">
      <MobileSidebar />
      <NavbarRoutes />
    </div>
  );
};

export default Navbar;
