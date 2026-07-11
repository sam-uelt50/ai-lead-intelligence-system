const express = require('express');
const router = express.Router();
const ScrapingOrchestrator = require('../services/ScrapingOrchestrator');
const ScrapedCompany = require('../models/ScrapedCompany');
require('dotenv').config();

const orchestrator = new ScrapingOrchestrator(process.env.GEMINI_API_KEY);

// Scrape single company
router.post('/company', async (req, res) => {
    try {
        const { url, companyName } = req.body;
        
        if (!url && !companyName) {
            return res.status(400).json({ error: 'URL or company name required' });
        }

        const target = url || companyName;
        
        // Check if already exists
        const existing = await ScrapedCompany.findOne({ 
            $or: [
                { website: url },
                { name: companyName },
                { domain: extractDomain(url) }
            ]
        });

        if (existing) {
            return res.json({
                message: 'Company already exists in database',
                data: existing,
                exists: true
            });
        }

        // Scrape new data
        const scrapedData = await orchestrator.scrapeCompany(target);
        
        // Save to database
        const savedCompany = await ScrapedCompany.create(scrapedData);
        
        res.json({
            message: 'Company scraped successfully',
            data: savedCompany,
            exists: false
        });

    } catch (error) {
        console.error('Scraping error:', error);
        res.status(500).json({ error: 'Scraping failed', details: error.message });
    }
});

// Batch scrape
router.post('/batch', async (req, res) => {
    try {
        const { urls } = req.body;
        
        if (!urls || !Array.isArray(urls)) {
            return res.status(400).json({ error: 'URLs array required' });
        }

        const results = await orchestrator.batchScrape(urls.slice(0, 10)); // Limit to 10
        
        // Save successful scrapes
        const savedCompanies = [];
        for (const result of results) {
            if (result.success) {
                const saved = await ScrapedCompany.create(result.data);
                savedCompanies.push(saved);
            }
        }

        res.json({
            message: `Batch scraping completed. ${savedCompanies.length} companies saved.`,
            total: urls.length,
            successful: savedCompanies.length,
            failed: results.filter(r => !r.success).length,
            results: results.map(r => ({
                url: r.url,
                success: r.success,
                companyId: r.success ? r.data._id : null
            }))
        });

    } catch (error) {
        res.status(500).json({ error: 'Batch scraping failed', details: error.message });
    }
});

// Get all scraped companies
router.get('/companies', async (req, res) => {
    try {
        const { 
            page = 1, 
            limit = 20, 
            industry, 
            status,
            sortBy = 'scrapedAt',
            order = 'desc'
        } = req.query;

        const filter = {};
        if (industry) filter.industry = industry;
        if (status) filter.status = status;

        const sort = {};
        sort[sortBy] = order === 'desc' ? -1 : 1;

        const companies = await ScrapedCompany.find(filter)
            .sort(sort)
            .limit(parseInt(limit))
            .skip((page - 1) * limit);

        const total = await ScrapedCompany.countDocuments(filter);

        res.json({
            page: parseInt(page),
            limit: parseInt(limit),
            total,
            pages: Math.ceil(total / limit),
            data: companies
        });

    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch companies' });
    }
});

// Update company status
router.patch('/company/:id/status', async (req, res) => {
    try {
        const { status } = req.body;
        const { id } = req.params;

        const validStatuses = ['pending', 'verified', 'rejected', 'duplicate'];
        if (!validStatuses.includes(status)) {
            return res.status(400).json({ error: 'Invalid status' });
        }

        const company = await ScrapedCompany.findByIdAndUpdate(
            id,
            { 
                status,
                verifiedAt: status === 'verified' ? new Date() : null
            },
            { new: true }
        );

        if (!company) {
            return res.status(404).json({ error: 'Company not found' });
        }

        res.json({
            message: `Company status updated to ${status}`,
            data: company
        });

    } catch (error) {
        res.status(500).json({ error: 'Failed to update status' });
    }
});

// Search companies
router.get('/search', async (req, res) => {
    try {
        const { q } = req.query;
        
        if (!q || q.length < 2) {
            return res.status(400).json({ error: 'Search query too short' });
        }

        const companies = await ScrapedCompany.find({
            $or: [
                { name: { $regex: q, $options: 'i' } },
                { description: { $regex: q, $options: 'i' } },
                { industry: { $regex: q, $options: 'i' } },
                { tags: { $regex: q, $options: 'i' } }
            ]
        }).limit(20);

        res.json({
            query: q,
            count: companies.length,
            data: companies
        });

    } catch (error) {
        res.status(500).json({ error: 'Search failed' });
    }
});

// Get company statistics
router.get('/stats', async (req, res) => {
    try {
        const totalCompanies = await ScrapedCompany.countDocuments();
        const verifiedCompanies = await ScrapedCompany.countDocuments({ status: 'verified' });
        
        const industries = await ScrapedCompany.aggregate([
            { $group: { _id: '$industry', count: { $sum: 1 } } },
            { $sort: { count: -1 } },
            { $limit: 10 }
        ]);

        const statusDistribution = await ScrapedCompany.aggregate([
            { $group: { _id: '$status', count: { $sum: 1 } } }
        ]);

        const monthlyGrowth = await ScrapedCompany.aggregate([
            {
                $group: {
                    _id: {
                        year: { $year: '$createdAt' },
                        month: { $month: '$createdAt' }
                    },
                    count: { $sum: 1 }
                }
            },
            { $sort: { '_id.year': 1, '_id.month': 1 } },
            { $limit: 12 }
        ]);

        res.json({
            total: totalCompanies,
            verified: verifiedCompanies,
            verificationRate: totalCompanies > 0 ? (verifiedCompanies / totalCompanies * 100).toFixed(1) : 0,
            topIndustries: industries,
            statusDistribution,
            monthlyGrowth
        });

    } catch (error) {
        res.status(500).json({ error: 'Failed to get statistics' });
    }
});

function extractDomain(url) {
    try {
        const urlObj = new URL(url);
        return urlObj.hostname.replace('www.', '');
    } catch (error) {
        return null;
    }
}

module.exports = router;