import React, { useState, useRef } from 'react';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  // Generate States
  const [prompt, setPrompt] = useState('');
  const [modelVersion, setModelVersion] = useState('Stable Diffusion');
  const [qualityLevel, setQualityLevel] = useState('High Quality');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [generateError, setGenerateError] = useState(null);

  // Verify States
  const fileInputRef = useRef(null);
  const [verifyFile, setVerifyFile] = useState(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [verifyData, setVerifyData] = useState(null);
  const [verifyError, setVerifyError] = useState(null);

  const API_BASE_URL = 'http://localhost:8000';

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setGenerateError("Lütfen bir resim açıklaması (prompt) girin.");
      return;
    }

    setIsGenerating(true);
    setGenerateError(null);
    setGeneratedImage(null);

    const formData = new FormData();
    formData.append('prompt', prompt);
    formData.append('model_version', modelVersion);
    formData.append('quality_level', qualityLevel);

    try {
      // In a real scenario with JWT auth, we would pass headers: { Authorization: `Bearer ${token}` }
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Resim üretilirken bir hata oluştu.");
      }

      setGeneratedImage(`${API_BASE_URL}${data.image_url}`);
    } catch (error) {
      setGenerateError(error.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleVerifyClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setVerifyFile(e.target.files[0]);
      setVerifyData(null);
      setVerifyError(null);
    }
  };

  const handleVerify = async () => {
    if (!verifyFile) {
      setVerifyError("Lütfen doğrulamak için bir görsel yükleyin.");
      return;
    }

    setIsVerifying(true);
    setVerifyError(null);
    setVerifyData(null);

    const formData = new FormData();
    formData.append('file', verifyFile);

    try {
      const response = await fetch(`${API_BASE_URL}/api/extract`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Görsel doğrulanırken bir hata oluştu.");
      }

      if (data.status === "failed") {
        throw new Error(data.message || "Filigran bulunamadı.");
      }

      setVerifyData(data.data);
    } catch (error) {
      setVerifyError(error.message);
    } finally {
      setIsVerifying(false);
    }
  };

  return (
    <div className="bg-white min-h-screen">
      <header className="w-full bg-white border-b border-gray-100 sticky top-0 z-50">
        <div className="w-full px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-8">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 flex items-center justify-center bg-primary rounded-lg">
                  <i className="ri-fingerprint-line text-white text-lg"></i>
                </div>
                <span className="text-2xl font-['Pacifico'] text-gray-900">TraceMark</span>
              </div>
              <nav className="hidden md:flex items-center space-x-8">
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">Generate</a>
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">Verify</a>
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">About</a>
                <a href="#" className="text-gray-700 hover:text-primary transition-colors">Documentation</a>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <a href="#login" className="text-gray-700 hover:text-primary transition-colors px-4 py-2 !rounded-button whitespace-nowrap">
                Sign In
              </a>
              <button className="bg-primary text-white px-6 py-2 !rounded-button hover:bg-blue-600 transition-colors whitespace-nowrap">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </header>

      <section className="w-full min-h-screen relative overflow-hidden" style={{ backgroundImage: "url('https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&w=1920&q=80')", backgroundSize: "cover", backgroundPosition: "center" }}>
        <div className="absolute inset-0 bg-gradient-to-r from-white via-white/95 to-transparent"></div>
        <div className="relative w-full px-6 py-20 flex items-center min-h-screen">
          <div className="w-full max-w-7xl mx-auto">
            <div className="max-w-2xl">
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
                Secure AI Image Generation with
                <span className="text-primary"> Built-in Provenance</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Enhance the traceability, authenticity, and accountability of AI-generated images with invisible, tamper-resistant watermarking technology. Verify origin, authorship, and generation context with confidence.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <button onClick={() => { setActiveTab('generate'); window.scrollTo(0, 800); }} className="bg-primary text-white px-8 py-4 !rounded-button hover:bg-blue-600 transition-colors text-lg font-semibold whitespace-nowrap">
                  Generate Images
                </button>
                <button onClick={() => { setActiveTab('verify'); window.scrollTo(0, 800); }} className="border-2 border-gray-300 text-gray-700 px-8 py-4 !rounded-button hover:border-primary hover:text-primary transition-colors text-lg font-semibold whitespace-nowrap">
                  Verify Images
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="w-full py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Dual-Function Platform</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Generate AI images with embedded metadata or verify existing images to reveal their provenance and authenticity
            </p>
          </div>
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div className="flex border-b border-gray-200">
              <button 
                onClick={() => setActiveTab('generate')}
                className={`flex-1 px-8 py-4 text-lg font-semibold transition-colors ${activeTab === 'generate' ? 'text-primary border-b-2 border-primary bg-blue-50' : 'text-gray-600 hover:text-primary'}`}
              >
                <div className="w-6 h-6 flex items-center justify-center inline-block mr-3">
                  <i className="ri-image-add-line text-xl"></i>
                </div>
                Generate & Watermark
              </button>
              <button 
                onClick={() => setActiveTab('verify')}
                className={`flex-1 px-8 py-4 text-lg font-semibold transition-colors ${activeTab === 'verify' ? 'text-primary border-b-2 border-primary bg-blue-50' : 'text-gray-600 hover:text-primary'}`}
              >
                <div className="w-6 h-6 flex items-center justify-center inline-block mr-3">
                  <i className="ri-shield-check-line text-xl"></i>
                </div>
                Verify & Extract
              </button>
            </div>
            
            {activeTab === 'generate' && (
              <div className="p-8">
                <div className="grid lg:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-3">Image Prompt</label>
                      <textarea 
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        className="w-full p-4 border border-gray-300 rounded-lg resize-none h-32 text-sm focus:ring-2 focus:ring-primary focus:border-primary" 
                        placeholder="Describe the image you want to generate..."
                        disabled={isGenerating}
                      ></textarea>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-3">Model Version</label>
                        <select 
                          value={modelVersion}
                          onChange={(e) => setModelVersion(e.target.value)}
                          disabled={isGenerating}
                          className="w-full p-3 border border-gray-300 rounded-lg text-left text-sm bg-white hover:border-primary transition-colors focus:ring-2 focus:ring-primary"
                        >
                          <option value="Stable Diffusion">Stable Diffusion XL</option>
                          <option value="DALL-E">DALL-E 3</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-3">Quality Level</label>
                        <select 
                          value={qualityLevel}
                          onChange={(e) => setQualityLevel(e.target.value)}
                          disabled={isGenerating}
                          className="w-full p-3 border border-gray-300 rounded-lg text-left text-sm bg-white hover:border-primary transition-colors focus:ring-2 focus:ring-primary"
                        >
                          <option value="High Quality">High Quality</option>
                          <option value="Standard">Standard</option>
                          <option value="Fast">Fast</option>
                        </select>
                      </div>
                    </div>
                    
                    {generateError && (
                      <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm border border-red-200">
                        <i className="ri-error-warning-line mr-2"></i>
                        {generateError}
                      </div>
                    )}

                    <button 
                      onClick={handleGenerate}
                      disabled={isGenerating}
                      className={`w-full text-white py-4 !rounded-button transition-colors font-semibold whitespace-nowrap flex items-center justify-center ${isGenerating ? 'bg-blue-400 cursor-not-allowed' : 'bg-primary hover:bg-blue-600'}`}
                    >
                      {isGenerating ? (
                        <>
                          <i className="ri-loader-4-line animate-spin text-xl mr-2"></i>
                          Generating & Watermarking...
                        </>
                      ) : (
                        'Generate with Watermark'
                      )}
                    </button>
                  </div>
                  <div className="bg-gray-50 rounded-xl p-6 flex items-center justify-center min-h-80 border border-gray-200 overflow-hidden">
                    {generatedImage ? (
                      <div className="text-center w-full">
                        <img src={generatedImage} alt="Generated" className="max-w-full h-auto rounded-lg shadow-sm mb-4 mx-auto max-h-[400px] object-contain" />
                        <a href={generatedImage} download="tracemark_generated.png" target="_blank" rel="noreferrer" className="text-primary hover:text-blue-700 text-sm font-medium">
                          <i className="ri-download-cloud-2-line mr-1"></i> Download Image
                        </a>
                      </div>
                    ) : (
                      <div className="text-center">
                        <div className="w-16 h-16 flex items-center justify-center mx-auto mb-4 bg-gray-200 rounded-full">
                          <i className="ri-image-line text-2xl text-gray-400"></i>
                        </div>
                        <p className="text-gray-500">Generated image will appear here</p>
                        <p className="text-sm text-gray-400 mt-2">With invisible watermark embedded</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'verify' && (
              <div className="p-8">
                <div className="grid lg:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <input 
                      type="file" 
                      ref={fileInputRef} 
                      onChange={handleFileChange} 
                      className="hidden" 
                      accept="image/*"
                    />
                    <div 
                      onClick={handleVerifyClick}
                      className={`border-2 border-dashed ${verifyFile ? 'border-primary bg-blue-50' : 'border-gray-300 hover:border-primary'} rounded-xl p-8 text-center transition-colors cursor-pointer`}
                    >
                      <div className="w-16 h-16 flex items-center justify-center mx-auto mb-4 bg-white shadow-sm border border-gray-100 rounded-full">
                        {verifyFile ? (
                          <i className="ri-image-2-line text-2xl text-primary"></i>
                        ) : (
                          <i className="ri-upload-cloud-2-line text-2xl text-gray-400"></i>
                        )}
                      </div>
                      <p className="text-lg font-semibold text-gray-700 mb-2">
                        {verifyFile ? verifyFile.name : "Upload Image to Verify"}
                      </p>
                      <p className="text-sm text-gray-500">
                        {verifyFile ? "Click to change file" : "Drag and drop or click to select"}
                      </p>
                      <p className="text-xs text-gray-400 mt-2">Supports JPG, PNG, WebP formats</p>
                    </div>

                    {verifyError && (
                      <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm border border-red-200">
                        <i className="ri-error-warning-line mr-2"></i>
                        {verifyError}
                      </div>
                    )}

                    <button 
                      onClick={handleVerify}
                      disabled={!verifyFile || isVerifying}
                      className={`w-full text-white py-4 !rounded-button transition-colors font-semibold whitespace-nowrap flex items-center justify-center ${(isVerifying || !verifyFile) ? 'bg-cyan-400 cursor-not-allowed' : 'bg-secondary hover:bg-cyan-600'}`}
                    >
                      {isVerifying ? (
                        <>
                          <i className="ri-loader-4-line animate-spin text-xl mr-2"></i>
                          Extracting Metadata...
                        </>
                      ) : (
                        'Extract Metadata'
                      )}
                    </button>
                  </div>
                  <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Metadata Results</h3>
                    
                    {verifyData ? (
                      <div className="space-y-4">
                        <div className="bg-white p-4 rounded-lg border border-green-200 shadow-sm">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-600">Verification Status</span>
                            <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full flex items-center">
                              <i className="ri-checkbox-circle-fill mr-1"></i> Verified
                            </span>
                          </div>
                        </div>
                        <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                          <span className="text-sm font-medium text-gray-600 block mb-1">Creator / User</span>
                          <span className="text-sm text-gray-900 font-semibold">{verifyData.creator}</span>
                        </div>
                        <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                          <span className="text-sm font-medium text-gray-600 block mb-1">Generation Time</span>
                          <span className="text-sm text-gray-900">{verifyData.date}</span>
                        </div>
                        <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                          <span className="text-sm font-medium text-gray-600 block mb-1">Model Version</span>
                          <span className="text-sm text-gray-900">{verifyData.model}</span>
                        </div>
                        <div className="mt-4 pt-4 border-t border-gray-200">
                           <span className="text-xs font-medium text-gray-500 block mb-1">Raw Extracted String</span>
                           <code className="text-xs text-gray-700 bg-gray-100 p-2 rounded block break-all">{verifyData.raw}</code>
                        </div>
                      </div>
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center min-h-[250px] text-gray-400">
                        <i className="ri-shield-check-line text-4xl mb-3 opacity-50"></i>
                        <p className="text-sm text-center">Results will appear here<br/>after verification</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      <section className="w-full py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Key Features</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Advanced watermarking technology meets practical verification needs
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center p-6 bg-gray-50 rounded-xl hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 flex items-center justify-center mx-auto mb-4 bg-blue-100 rounded-full">
                <i className="ri-eye-off-line text-2xl text-primary"></i>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Invisible Watermarking</h3>
              <p className="text-sm text-gray-600">Embed metadata without affecting visual quality or image aesthetics</p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-xl hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 flex items-center justify-center mx-auto mb-4 bg-green-100 rounded-full">
                <i className="ri-shield-check-line text-2xl text-green-600"></i>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Tamper Resistant</h3>
              <p className="text-sm text-gray-600">Advanced algorithms protect against manipulation and unauthorized changes</p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-xl hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 flex items-center justify-center mx-auto mb-4 bg-purple-100 rounded-full">
                <i className="ri-time-line text-2xl text-purple-600"></i>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Real-time Verification</h3>
              <p className="text-sm text-gray-600">Instant metadata extraction and authenticity verification</p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-xl hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 flex items-center justify-center mx-auto mb-4 bg-orange-100 rounded-full">
                <i className="ri-user-line text-2xl text-orange-600"></i>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Identity Protection</h3>
              <p className="text-sm text-gray-600">Secure creator identification while maintaining privacy controls</p>
            </div>
          </div>
        </div>
      </section>

      <section className="w-full py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              A simple two-stage process for generation and verification
            </p>
          </div>
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="flex items-start space-x-4">
                <div className="w-10 h-10 flex items-center justify-center bg-primary text-white rounded-full font-bold text-lg flex-shrink-0">1</div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Generate with Metadata</h3>
                  <p className="text-gray-600">Input your text prompt and generate AI images using advanced diffusion models. Our watermarking algorithm invisibly embeds creator identity, timestamp, and model version directly into the image pixels.</p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="w-10 h-10 flex items-center justify-center bg-secondary text-white rounded-full font-bold text-lg flex-shrink-0">2</div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">Verify and Extract</h3>
                  <p className="text-gray-600">Upload any image to our verification portal. The system extracts and displays embedded metadata, revealing key information about the image's origin, generation history, and authenticity status.</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-xl p-8 shadow-lg">
              <img src="https://images.unsplash.com/photo-1633265486064-086b219458ce?auto=format&fit=crop&w=600&q=80" alt="TraceMark Workflow" className="w-full h-80 object-cover object-center rounded-lg" />
            </div>
          </div>
        </div>
      </section>

      <footer className="w-full bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="col-span-1">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-8 h-8 flex items-center justify-center bg-primary rounded-lg">
                  <i className="ri-fingerprint-line text-white text-lg"></i>
                </div>
                <span className="text-2xl font-['Pacifico']">TraceMark</span>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed">
                Enhancing AI image authenticity through advanced watermarking and verification technology.
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Platform</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Generate Images</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Verify Images</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Access</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Research Papers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">© 2026 TraceMark. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
