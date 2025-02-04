"use client";

import {
  Book,
  CircleCheck,
  Compass,
  Notebook,
  Settings,
  User,
} from "lucide-react";

import SidebarItem from "./sidebar-item";

const routes = [
  {
    label: "Dashboard",
    href: "/admin/dashboard",
    icon: Compass,
  },
  {
    label: "Staff",
    href: "/admin/staff",
    icon: User,
  },
  {
    label: "Courses",
    href: "/admin/courses",
    icon: Book,
  },
  {
    label: "Content",
    href: "/admin/content",
    icon: Notebook,
  },
  {
    label: "Tickets",
    href: "/admin/tickets",
    icon: CircleCheck,
  },
  {
    label: "Settings",
    href: "/admin/settings",
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
