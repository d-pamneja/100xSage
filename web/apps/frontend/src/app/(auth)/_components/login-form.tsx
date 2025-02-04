"use client";
import { Lock, User } from "lucide-react";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { signIn } from "next-auth/react";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { toast } from "sonner";

const formSchema = z.object({
  username: z.string().nonempty({ message: "Username is required" }),
  password: z.string().nonempty({ message: "Password is required" }),
});

const LoginForm = () => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    const resp = await signIn("credentials", {
      username: data.username,
      password: data.password,
      redirect: true,
      redirectTo: "/admin/dashboard",
    });
    if (resp?.error) {
      form.setError(
        "password",
        { message: "Invalid username or password" },
        { shouldFocus: true },
      );
      toast.error("Failed to sign in");
    }
  };

  return (
    <div className="flex w-full">
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="mt-4 flex w-full flex-col gap-6"
        >
          <FormField
            name="username"
            control={form.control}
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <div className="flex h-[52px] w-full items-center rounded-lg bg-[#F5F5F5] px-4 py-2">
                    <User className="mr-2 text-[#b2b2b2]" />
                    <input
                      {...field}
                      placeholder="Username"
                      className="input-autofill w-full bg-transparent text-black placeholder-[#4c4c4c] focus:outline-none"
                      style={
                        {
                          "--autofill-text-color": "black",
                        } as React.CSSProperties
                      }
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            name="password"
            control={form.control}
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <div className="flex h-[52px] w-full items-center rounded-lg bg-[#F5F5F5] px-4 py-2">
                    <Lock className="mr-2 text-[#b2b2b2]" />
                    <input
                      {...field}
                      type="password"
                      placeholder="Password"
                      className="input-autofill w-full bg-transparent text-black placeholder-[#4c4c4c] focus:outline-none"
                      style={
                        {
                          "--autofill-text-color": "black",
                        } as React.CSSProperties
                      }
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormMessage />
          <button className="m-auto flex w-full" type="submit">
            <div className="h-[52px] w-full rounded-full bg-[#1B1B1B]">
              <div className="flex h-full w-full items-center justify-center font-normal text-white">
                Login
              </div>
            </div>
          </button>
        </form>
      </Form>
    </div>
  );
};

export default LoginForm;
