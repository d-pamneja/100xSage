"use client";
import { Key, Lock, MailIcon } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { useSearchParams } from "next/navigation";
import { signUpUser } from "@/actions/auth/signup-user";
import { useRouter } from "next/navigation";
const formSchema = z.object({
  username: z.string().nonempty({ message: "Username is required" }),
  password: z.string().nonempty({ message: "Password is required" }),
  confirmPassword: z
    .string()
    .nonempty({ message: "Confirm Password is required" }),
});

const SignupForm = () => {
  const params = useSearchParams();
  const router = useRouter();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
      confirmPassword: "",
    },
  });
  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    if (data.password != data.confirmPassword) {
      form.setError(
        "confirmPassword",
        { message: "Passwords do not match" },
        { shouldFocus: true },
      );
      return;
    }
    const resp = await signUpUser({
      username: data.username,
      password: data.password,
    });
    if (resp.status === 200) {
      toast.success("Account created successfully");
      router.push("/login");
    } else if (resp.status == 409) {
      form.setError(
        "username",
        { message: "Username already taken" },
        { shouldFocus: true },
      );
    } else {
      toast.error("Failed to create account");
    }
  };
  return (
    <div className="flex w-full overflow-auto">
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
                    <MailIcon className="mr-2 text-[#b2b2b2]" />
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
                      placeholder="Password"
                      type="password"
                      style={
                        {
                          "--autofill-text-color": "black",
                        } as React.CSSProperties
                      }
                      className="input-autofill w-full bg-transparent text-black placeholder-[#4c4c4c] focus:outline-none"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            name="confirmPassword"
            control={form.control}
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <div className="flex h-[52px] w-full items-center rounded-lg bg-[#F5F5F5] px-4 py-2">
                    <Key className="mr-2 text-[#b2b2b2]" />
                    <input
                      {...field}
                      placeholder="Confirm Password"
                      type="password"
                      style={
                        {
                          "--autofill-text-color": "black",
                        } as React.CSSProperties
                      }
                      className="input-autofill w-full bg-transparent text-black placeholder-[#4c4c4c] focus:outline-none"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          {params.get("error") && (
            <div className="text-sm text-red-500">
              Error: {params.get("error")}
            </div>
          )}
          <button className="m-auto flex w-full" type="submit">
            <div className="h-[52px] w-full rounded-full bg-[#1B1B1B]">
              <div className="flex h-full w-full items-center justify-center font-normal text-white">
                Sign Up
              </div>
            </div>
          </button>
        </form>
      </Form>
    </div>
  );
};

export default SignupForm;
