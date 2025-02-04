"use client";

import { Compass } from "lucide-react";

import SidebarItem from "./sidebar-item";

const routes = [
  {
    icon: Compass,
    label: "Dashboard",
    href: "/admin/dashboard",
  },
];
const SidebarRoutes = () => {
  return (
    <div className="flex w-full flex-col">
      {routes.map((route) => (
        <SidebarItem
          key={route.label}
          icon={route.icon}
          label={route.label}
          href={route.href}
        />
      ))}
    </div>
  );
};

export default SidebarRoutes;
