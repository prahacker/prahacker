import { Card } from "@/components/ui/card"

export default function Component() {
  return (
    <Card className="w-full max-w-3xl mx-auto p-6 bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <h1 className="text-4xl font-bold mb-4">👋 Hi there, I'm [Your Name]</h1>
      <p className="text-xl mb-6">A passionate developer always learning and creating</p>
      
      <h2 className="text-2xl font-semibold mb-4">🚀 Latest Projects</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Project cards will be dynamically inserted here */}
        {`<!-- PROJECTS_PLACEHOLDER -->`}
      </div>
      
      <h2 className="text-2xl font-semibold mt-8 mb-4">📊 GitHub Stats</h2>
      <img src="https://github-readme-stats.vercel.app/api?username=yourusername&show_icons=true&theme=radical" alt="GitHub Stats" className="w-full max-w-md mx-auto" />
      
      <h2 className="text-2xl font-semibold mt-8 mb-4">🔗 Connect with me</h2>
      <div className="flex space-x-4">
        <a href="https://twitter.com/yourusername" className="text-blue-400 hover:text-blue-300">Twitter</a>
        <a href="https://linkedin.com/in/yourusername" className="text-blue-400 hover:text-blue-300">LinkedIn</a>
        <a href="https://yourblog.com" className="text-blue-400 hover:text-blue-300">Blog</a>
      </div>
    </Card>
  )
}
