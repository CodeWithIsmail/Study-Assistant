# Study Assistant Frontend

A beautiful and modern React frontend for the Study Assistant RAG chatbot.

## Features

- 🎨 Modern, responsive design with Tailwind CSS
- 💬 Real-time chat interface
- 🌓 Dark/light mode support
- 📱 Mobile-friendly responsive design
- 🔗 Source document references
- ⚡ Real-time connection status
- 🎭 Smooth animations and loading states

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Study Assistant backend running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Usage

1. Make sure the backend server is running on `http://localhost:8000`
2. Type your questions in the chat input
3. Get AI-powered answers based on your uploaded documents
4. View source references for each answer

## API Configuration

The frontend expects the backend to be running on `http://localhost:8000`. You can modify this in `src/services/api.ts` if needed.

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Technology Stack

- **React 19** - Frontend framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Axios** - HTTP client
- **Lucide React** - Icons
