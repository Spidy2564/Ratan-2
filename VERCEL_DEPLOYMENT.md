# Vercel Deployment Guide

This guide will help you deploy your Wallet Platform to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Git Repository**: Your project should be in a Git repository (GitHub, GitLab, etc.)
3. **Node.js**: Install Node.js on your local machine

## Quick Deployment

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push to Git**: Make sure your code is pushed to your Git repository
2. **Import Project**: 
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your Git repository
3. **Configure Project**:
   - Framework Preset: `Other`
   - Root Directory: `./` (or leave empty)
   - Build Command: Leave empty
   - Output Directory: Leave empty
4. **Deploy**: Click "Deploy"

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `wallet-platform` (or your preferred name)
   - In which directory: `./` (or leave empty)
   - Want to override settings: `N`

## Project Structure for Vercel

```
wallet/
├── api/                    # Serverless functions
│   ├── __init__.py
│   ├── connect.py         # POST /api/connect
│   ├── connections.py     # GET/POST /api/connections/[id]
│   └── stats.py          # GET /api/stats
├── frontend/              # Static files
│   ├── index.html        # Main page
│   ├── admin.html        # Admin dashboard
│   ├── connect.html      # Connection page
│   ├── mobile.html       # Mobile page
│   └── app.js           # Frontend logic
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── package.json         # Node.js dependencies
```

## API Endpoints

The platform provides these serverless API endpoints:

- **POST** `/api/connect` - Create new wallet connection
- **GET** `/api/connections/[id]` - Get connection status
- **POST** `/api/connections/[id]` - Update connection
- **GET** `/api/stats` - Get platform statistics

## Database Storage

**Important**: Vercel serverless functions have read-only filesystem access. For production use, you'll need to:

1. **Use a Database Service**:
   - [Vercel KV](https://vercel.com/docs/storage/vercel-kv) (Redis)
   - [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres)
   - [MongoDB Atlas](https://www.mongodb.com/atlas)
   - [Supabase](https://supabase.com)

2. **Update API Functions**: Replace file-based storage with database calls

## Environment Variables

Set these in your Vercel project settings:

```bash
# Optional: Database connection strings
DATABASE_URL=your_database_connection_string

# Optional: Secret key for JWT tokens
SECRET_KEY=your_secret_key
```

## Custom Domain

1. **Add Domain**: Go to your project settings → Domains
2. **Configure DNS**: Follow Vercel's DNS configuration instructions
3. **SSL**: Vercel automatically provides SSL certificates

## Monitoring & Analytics

- **Vercel Analytics**: Built-in performance monitoring
- **Function Logs**: View serverless function execution logs
- **Performance**: Monitor API response times and errors

## Troubleshooting

### Common Issues

1. **API Functions Not Working**:
   - Check function logs in Vercel dashboard
   - Verify `vercel.json` routing configuration
   - Ensure Python dependencies are correct

2. **CORS Errors**:
   - API functions include CORS headers
   - Check browser console for specific errors

3. **Database Issues**:
   - Remember: Vercel functions can't write to local files
   - Use external database service for production

4. **Build Failures**:
   - Check `requirements.txt` for compatible versions
   - Verify Python runtime compatibility

### Debug Mode

For local development and testing:

```bash
# Install Vercel CLI
npm i -g vercel

# Run locally
vercel dev

# This will start local development server
# Access at http://localhost:3000
```

## Production Considerations

1. **Database**: Use production database service
2. **Security**: Implement proper authentication
3. **Rate Limiting**: Add API rate limiting
4. **Monitoring**: Set up error tracking and analytics
5. **Backup**: Regular database backups

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Project Issues**: Check the project repository for known issues

## Next Steps

After successful deployment:

1. **Test All Features**: Verify wallet connections work
2. **Set Up Database**: Implement proper data storage
3. **Add Authentication**: Secure admin dashboard
4. **Monitor Performance**: Track usage and errors
5. **Scale**: Optimize for increased traffic

---

**Note**: This deployment guide assumes you're using the current project structure. Adjust paths and configurations as needed for your specific setup.
