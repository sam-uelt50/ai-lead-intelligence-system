const axios = require('axios');

class DataEnrichmentService {
    constructor(geminiApiKey) {
        this.geminiApiKey = geminiApiKey;
        this.geminiUrl = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';
    }

    async enrichWithAI(companyData) {
        try {
            const prompt = this.createEnrichmentPrompt(companyData);
            
            const response = await axios.post(
                `${this.geminiUrl}?key=${this.geminiApiKey}`,
                {
                    contents: [{
                        parts: [{ text: prompt }]
                    }]
                },
                {
                    headers: { 'Content-Type': 'application/json' }
                }
            );

            const aiResponse = response.data.candidates[0].content.parts[0].text;
            return this.parseAIResponse(aiResponse, companyData);
            
        } catch (error) {
            console.error('AI enrichment error:', error.message);
            return companyData;
        }
    }

    createEnrichmentPrompt(companyData) {
        return `
        Analyze this company data and provide enriched information:
        
        Company: ${companyData.name}
        Industry: ${companyData.industry || 'Unknown'}
        Description: ${companyData.description || 'No description'}
        Website: ${companyData.website || 'Unknown'}
        
        Please provide:
        1. A professional 2-3 paragraph company description
        2. Suggested tags/categories (comma separated)
        3. Target customer profile
        4. Key value propositions
        5. Growth stage estimation (Startup, Growth, Mature, Enterprise)
        
        Format response as JSON:
        {
            "enhancedDescription": "detailed description here",
            "tags": ["tag1", "tag2"],
            "targetCustomers": "description",
            "valuePropositions": ["prop1", "prop2"],
            "growthStage": "Startup|Growth|Mature|Enterprise"
        }
        `;
    }

    parseAIResponse(aiResponse, originalData) {
        try {
            // Try to extract JSON from response
            const jsonMatch = aiResponse.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                const enriched = JSON.parse(jsonMatch[0]);
                return {
                    ...originalData,
                    aiGeneratedDescription: enriched.enhancedDescription,
                    tags: [...(originalData.tags || []), ...enriched.tags],
                    targetCustomers: enriched.targetCustomers,
                    valuePropositions: enriched.valuePropositions,
                    growthStage: enriched.growthStage,
                    enrichedWithAI: true
                };
            }
        } catch (error) {
            console.error('Failed to parse AI response:', error);
        }
        
        return {
            ...originalData,
            aiGeneratedDescription: aiResponse,
            enrichedWithAI: true
        };
    }

    async cleanAndValidate(data) {
        // Data cleaning and validation
        const cleaned = { ...data };
        
        // Clean website URL
        if (cleaned.website && !cleaned.website.startsWith('http')) {
            cleaned.website = `https://${cleaned.website}`;
        }
        
        // Validate email
        if (cleaned.email && !this.validateEmail(cleaned.email)) {
            delete cleaned.email;
        }
        
        // Normalize employee range
        if (cleaned.employeesRange) {
            cleaned.employeesRange = this.normalizeEmployeeRange(cleaned.employeesRange);
        }
        
        // Calculate data quality score
        cleaned.dataQuality = {
            completeness: this.calculateCompletenessScore(cleaned),
            accuracy: 80, // Placeholder
            freshness: 100 // Just scraped
        };
        
        return cleaned;
    }

    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    normalizeEmployeeRange(range) {
        const ranges = {
            '1-10': '1-10',
            '11-50': '11-50',
            '51-200': '51-200',
            '201-500': '201-500',
            '501-1000': '501-1000',
            '1001-5000': '1001-5000',
            '5001-10000': '5001-10000',
            '10000+': '10000+'
        };
        
        // Try to match with known ranges
        for (const [key, value] of Object.entries(ranges)) {
            if (range.includes(key) || range.includes(value)) {
                return value;
            }
        }
        
        return range;
    }

    calculateCompletenessScore(data) {
        const requiredFields = ['name', 'website', 'industry'];
        const importantFields = ['description', 'employeesRange', 'headquarters', 'email'];
        
        let score = 0;
        let total = requiredFields.length + importantFields.length;
        
        requiredFields.forEach(field => {
            if (data[field] && data[field].trim()) score += 2;
        });
        
        importantFields.forEach(field => {
            if (data[field] && data[field].trim()) score += 1;
        });
        
        return Math.round((score / total) * 100);
    }
}

module.exports = DataEnrichmentService;