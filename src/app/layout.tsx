import React from 'react';
import './style.css';
export const metadata={title:'Digital Lab — AI Studio',description:'Atelier de production pédagogique'};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="fr"><body>{children}</body></html>;}
