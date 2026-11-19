# MeepleOS

System wspomagający zarządzanie lokalem z grami planszowymi (wypożyczalnia gier, zamówienia stolikowe, panel barowy/kuchenny KDS).

Projekt pracy inżynierskiej realizowany na Uniwersytecie Rzeszowskim pod kierunkiem dr. inż. Wojciecha Kozioła.

## Architektura i technologie

- **Backend:** .NET 10 LTS (C# 14, ASP.NET Core REST API, Entity Framework Core 10, PostgreSQL 17, SignalR)
- **Panel baru / KDS (Web):** React 19 + TypeScript + Vite, Tailwind CSS (komunikacja z czytnikiem RFID USB przez WebHID API)
- **Aplikacja mobilna klienta:** React Native (New Architecture: Fabric & TurboModules) + TypeScript (skanowanie tagów NFC gier, zamówienia stolikowe, Photo Evidence)

## Struktura projektu

- `diagrams/` – modele UML w Software Ideas Modeler (`.simp`) i wyeksportowane diagramy (Przypadki Użycia, Aktywności, Wymagania)
- `docs/` – dokumentacja projektowa i sprawozdania (`.docx`, `.pdf`)
- `specs/` – specyfikacje wymagań, architektura i notatki projektowe
- `research/` – integracja z API BoardGameGeek (XML API2), zbiory danych gier oraz skrypty pomocnicze
- `src/` – kod źródłowy aplikacji
