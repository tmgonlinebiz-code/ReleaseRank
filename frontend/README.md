# ReleaseRank Frontend

React + TypeScript frontend application for ReleaseRank.

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable React components
│   ├── pages/            # Page components
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API client services
│   ├── types/            # TypeScript type definitions
│   ├── styles/           # Global styles
│   ├── App.tsx           # Main App component
│   └── main.tsx          # Entry point
├── public/               # Static assets
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```