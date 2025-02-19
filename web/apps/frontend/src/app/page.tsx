import Container from "@/components/container";
import { Button } from "@/components/ui/button";
import Header from "@/sections/landing/Header";

import Link from "next/link";
import HeroSection from "./_components/hero-section";
import FeatureList from "./_components/feature-list";
import CardGrid from "./_components/card-grid";
import HeroImage from "./_components/hero-image";
import Hero from "@/sections/landing/Hero";

export default function LandingPage() {
  return (
    <div className="">
      <Header/>
      <Container>
        <main className="mx-4 my-4">
          <Hero/>
        </main>
      </Container>
      {/* <Container>
        <main className="mx-auto max-w-5xl">
          <FeatureList />
          <CardGrid />
        </main>
      </Container>
      <Container>
        <footer className="mx-auto mb-20 max-w-5xl">
          <div className="mt-16 flex flex-col gap-4 text-start">
            <h2 className="text-3xl font-semibold">
              🚀 Ready to supercharge your cohort with AI?
            </h2>
            <div className="mt-4 flex gap-4">
              <Link href={"/signup"}>
                <Button className="bg-white">Get Started</Button>
              </Link>
              <Link href={"/login"}>
                <Button
                  variant="outline"
                  className="border-gray-300 text-gray-300"
                >
                  Login
                </Button>
              </Link>
            </div>
          </div>
        </footer>
      </Container> */}
    </div>
  );
}
