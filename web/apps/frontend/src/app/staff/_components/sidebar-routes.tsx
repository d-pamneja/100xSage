"use client";

import { Book, CircleCheck, Compass, Notebook, Settings } from "lucide-react";

import SidebarItem from "./sidebar-item";

const routes = [
  {
    label: "Dashboard",
    href: "/staff/dashboard",
    icon: Compass,
  },
  {
    label: "Courses",
    href: "/staff/courses",
    icon: Book,
  },
  {
    label: "Content",
    href: "/staff/content",
    icon: Notebook,
  },
  {
    label: "Tickets",
    href: "/staff/tickets",
    icon: CircleCheck,
  },
  {
    label: "Settings",
    href: "/staff/settings",
    icon: Settings,
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
