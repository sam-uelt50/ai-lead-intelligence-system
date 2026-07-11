const BaseScraper = require('./BaseScraper');

class LinkedInScraper extends BaseScraper {
    constructor(apiKey) {
        super();
        this.apiKey = apiKey;
        this.baseUrl = 'https://www.linkedin.com/company';
    }

    async scrapeCompany(companyNameOrUrl) {
        let companyUrl;
        
        if (companyNameOrUrl.includes('linkedin.com')) {
            companyUrl = companyNameOrUrl;
        } else {
            companyUrl = `${this.baseUrl}/${this.slugify(companyNameOrUrl)}`;
        }

        console.log(`Scraping LinkedIn: ${companyUrl}`);
        
        try {
            const $ = await this.fetchPage(companyUrl);
            if (!$) return null;

            const companyData = {
                name: this.extractName($),
                description: this.extractDescription($),
                website: this.extractWebsite($),
                industry: this.extractIndustry($),
                headquarters: this.extractHeadquarters($),
                employeesRange: this.extractEmployees($),
                foundedYear: this.extractFoundedYear($),
                linkedinUrl: companyUrl,
                specialities: this.extractSpecialities($),
                socialMedia: this.extractSocialMedia($)
            };

            return this.validateCompanyData(companyData);
        } catch (error) {
            console.error(`LinkedIn scraping error: ${error.message}`);
            return null;
        }
    }

    slugify(text) {
        return text
            .toLowerCase()
            .replace(/[^\w\s]/g, '')
            .replace(/\s+/g, '-');
    }

    extractName($) {
        return $('h1').first().text().trim() || 
               $('title').text().split('|')[0].trim();
    }

    extractDescription($) {
        return $('.description').text().trim() ||
               $('meta[name="description"]').attr('content') ||
               $('.about-us').text().trim();
    }

    extractWebsite($) {
        return $('a[data-tracking-control-name="about_website"]').attr('href') ||
               $('a:contains("Website")').attr('href');
    }

    extractIndustry($) {
        return $('.industry').text().trim() ||
               $('dd:contains("Industry")').next().text().trim();
    }

    extractHeadquarters($) {
        return $('.headquarters').text().trim() ||
               $('dd:contains("Headquarters")').next().text().trim();
    }

    extractEmployees($) {
        const employeesText = $('.employees-on-linkedin').text() ||
                             $('dd:contains("Company size")').next().text();
        
        if (employeesText.includes('employees')) {
            const match = employeesText.match(/(\d+,\d+|\d+)\s*employees/i);
            if (match) return match[1];
        }
        return null;
    }

    extractFoundedYear($) {
        const foundedText = $('.founded').text() ||
                           $('dd:contains("Founded")').next().text();
        
        const yearMatch = foundedText.match(/\b(19|20)\d{2}\b/);
        return yearMatch ? parseInt(yearMatch[0]) : null;
    }

    extractSpecialities($) {
        const specialities = [];
        $('.specialities li, .specialty').each((i, el) => {
            specialities.push($(el).text().trim());
        });
        return specialities;
    }

    extractSocialMedia($) {
        const social = {};
        $('a[href*="twitter.com"]').each((i, el) => {
            social.twitter = $(el).attr('href');
        });
        $('a[href*="facebook.com"]').each((i, el) => {
            social.facebook = $(el).attr('href');
        });
        return social;
    }

    validateCompanyData(data) {
        // Add validation logic
        if (!data.name || !data.website) return null;
        return data;
    }
}

module.exports = LinkedInScraper;