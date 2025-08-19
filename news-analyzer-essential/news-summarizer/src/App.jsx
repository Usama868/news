import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, FileText, Link, Sparkles, MessageSquare, BarChart3 } from 'lucide-react'
import './App.css'

function App() {
  const [inputType, setInputType] = useState('text')
  const [newsContent, setNewsContent] = useState('')
  const [newsUrl, setNewsUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    setResult(null)

    try {
      const content = inputType === 'url' ? newsUrl : newsContent
      if (!content.trim()) {
        throw new Error('براہ کرم خبر کا متن یا لنک داخل کریں')
      }

      const response = await fetch('/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: inputType,
          content: content.trim()
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'کچھ خرابی ہوئی ہے')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2 flex items-center justify-center gap-3">
            <Sparkles className="text-blue-600" />
            خبروں کا تجزیہ کار
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Professional News Analysis & Lower Thirds Generator
          </p>
        </div>

        {/* Input Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="w-5 h-5" />
              خبر داخل کریں
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Tabs value={inputType} onValueChange={setInputType}>
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="text" className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    متن
                  </TabsTrigger>
                  <TabsTrigger value="url" className="flex items-center gap-2">
                    <Link className="w-4 h-4" />
                    لنک
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="text" className="space-y-4">
                  <Textarea
                    placeholder="یہاں خبر کا مکمل متن پیسٹ کریں..."
                    value={newsContent}
                    onChange={(e) => setNewsContent(e.target.value)}
                    className="min-h-[200px] text-right"
                    dir="rtl"
                  />
                </TabsContent>
                
                <TabsContent value="url" className="space-y-4">
                  <Input
                    type="url"
                    placeholder="https://example.com/news-article"
                    value={newsUrl}
                    onChange={(e) => setNewsUrl(e.target.value)}
                    className="text-left"
                    dir="ltr"
                  />
                </TabsContent>
              </Tabs>

              {error && (
                <div className="text-red-600 bg-red-50 dark:bg-red-900/20 p-3 rounded-md text-right" dir="rtl">
                  {error}
                </div>
              )}

              <Button 
                type="submit" 
                disabled={isLoading}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    تجزیہ کیا جا رہا ہے...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    تجزیہ شروع کریں
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Title and Sources */}
            <Card>
              <CardHeader>
                <CardTitle className="text-right" dir="rtl">{result.title}</CardTitle>
                {result.sources && result.sources.length > 0 && (
                  <div className="flex flex-wrap gap-2 justify-end">
                    {result.sources.map((source, index) => (
                      <Badge key={index} variant="secondary">
                        <a href={source.url} target="_blank" rel="noopener noreferrer">
                          {source.name}
                        </a>
                      </Badge>
                    ))}
                  </div>
                )}
              </CardHeader>
            </Card>

            {/* Lower Thirds */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 justify-end" dir="rtl">
                  <BarChart3 className="w-5 h-5" />
                  لوئر تھرڈز (LTs)
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.lower_thirds && result.lower_thirds.map((lt, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-50 dark:bg-gray-800 p-3 rounded-md">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyToClipboard(lt)}
                        className="ml-2"
                      >
                        Copy
                      </Button>
                      <div className="text-right flex-1" dir="rtl">
                        <Badge variant="outline" className="mr-2">{index + 1}</Badge>
                        {lt}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Questions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 justify-end" dir="rtl">
                  <MessageSquare className="w-5 h-5" />
                  پینل/ناظرین کے سوالات
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.questions && result.questions.map((question, index) => (
                    <div key={index} className="flex items-start justify-between bg-gray-50 dark:bg-gray-800 p-3 rounded-md">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyToClipboard(question)}
                        className="ml-2 mt-1"
                      >
                        Copy
                      </Button>
                      <div className="text-right flex-1" dir="rtl">
                        <Badge variant="outline" className="mr-2">{index + 1}</Badge>
                        {question}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Analysis */}
            {result.analysis && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-right" dir="rtl">تفصیلی تجزیہ اور مشاہدہ</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {result.analysis.lt_selection && (
                    <div>
                      <h4 className="font-semibold text-right mb-2" dir="rtl">LTs کا انتخاب:</h4>
                      <p className="text-gray-700 dark:text-gray-300 text-right" dir="rtl">
                        {result.analysis.lt_selection}
                      </p>
                    </div>
                  )}
                  
                  {result.analysis.question_importance && (
                    <div>
                      <h4 className="font-semibold text-right mb-2" dir="rtl">سوالات کی اہمیت:</h4>
                      <p className="text-gray-700 dark:text-gray-300 text-right" dir="rtl">
                        {result.analysis.question_importance}
                      </p>
                    </div>
                  )}
                  
                  {result.analysis.observations && (
                    <div>
                      <h4 className="font-semibold text-right mb-2" dir="rtl">مشاہدات اور پہلو:</h4>
                      <p className="text-gray-700 dark:text-gray-300 text-right" dir="rtl">
                        {result.analysis.observations}
                      </p>
                    </div>
                  )}
                  
                  {result.analysis.professional_standards && (
                    <div>
                      <h4 className="font-semibold text-right mb-2" dir="rtl">پروفیشنل معیار:</h4>
                      <p className="text-gray-700 dark:text-gray-300 text-right" dir="rtl">
                        {result.analysis.professional_standards}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App

