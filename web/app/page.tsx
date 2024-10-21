'use client';

import Link from 'next/link';

import SignInSection from './components/SignInSection';
import LogoImageHandler from './components/LogoImageHandler';
import { LoadingScreen } from './components/LoadingScreen';

import useUser from './hooks/useUser';

export default function Welcome() {
  const { isLoading } = useUser();

  if (isLoading) return <LoadingScreen />;

  return (
    <main className="flex flex-col flat:flex-row justify-center items-center gap-8 text-white p-8 h-screen w-screen bg-primary">
      <LogoImageHandler />
      <div className="flex flex-col gap-2">
        <div>
          <span className="text-2xl font-bold">Bem-vindos ao</span>
          <h1 className="flex flex-col text-6xl font-bold">
            <span>Sua Grade</span>
            <span>UnB</span>
          </h1>
        </div>
        <div className="grid grid-cols-3">
          <p className="col-span-2 font-semibold text-base">
            A ferramenta definitiva para os alunos da Universidade de Brasília
            planejarem suas trajetórias acadêmicas!
          </p>
        </div>
      </div>
      <div className="flex flex-col justify-center items-center gap-3">
        <SignInSection />
        <Link
          href="/schedules/home"
          className="font-bold underline underline-offset-2 flat:text-center"
        >
          Continuar como anônimo
        </Link>
      </div>
    </main>
  );
}
