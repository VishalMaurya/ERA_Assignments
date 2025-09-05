# Troubleshooting Guide

## Report Generation Issues

### "Invalid API key format" Error

**Cause**: Your Gemini API key format is incorrect.

**Solution**: 
1. Ensure your API key starts with "AIza"
2. Check that the key is at least 30 characters long
3. Get a new API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### "API quota exceeded" Error

**Cause**: You've reached your API usage limit.

**Solutions**:
- Wait for your quota to reset (usually resets daily)
- Check your billing settings in Google Cloud Console
- Consider upgrading your API plan if needed

### "Network error" Issues

**Cause**: Connection problems.

**Solutions**:
- Check your internet connection
- Try again in a few moments
- Ensure no firewall is blocking the connection

### "API access denied" Error

**Cause**: Your API key doesn't have proper permissions.

**Solutions**:
- Ensure the API key has Generative AI permissions
- Check that the key is enabled for the Gemini API
- Regenerate the API key if needed

### "Content was blocked by safety filters" Error

**Cause**: Your responses triggered AI safety filters.

**Solutions**:
- Review your assessment responses for potentially sensitive content
- Try rephrasing any responses that might be flagged
- Contact support if you believe this is an error

## Getting Help

1. **Check the Console**: Open browser developer tools to see detailed error messages
2. **Verify API Key**: Ensure your Gemini API key is valid and has proper permissions
3. **Test API Key**: Try using your API key directly in Google AI Studio to verify it works
4. **Network Issues**: Try from a different network if you suspect connectivity issues

## API Key Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key (starts with "AIza")
4. Paste it in the application when prompted
5. Ensure the key has Generative AI API access enabled
6. Verify access to Gemini 2.0 Flash model

## Still Having Issues?

If you continue to experience problems:
- Check the browser console for detailed error messages
- Ensure you're using the latest version of the application
- Try clearing browser cache and cookies
- Contact support with the specific error message you're receiving
