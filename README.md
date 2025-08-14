# Open WebUI RAG Output Formats Patch

This repository contains modifications to add RAG Output Formats support to [Open WebUI](https://github.com/open-webui/open-webui).

## What This Patch Adds

### 🎯 **RAG Output Formats System**
- **5 output formats**: Compact, Detailed, Academic, Table, List
- **3 configuration levels**: Per-Chat, Per-User, Global
- **Smart template selection** based on user preferences

### 🔧 **Backend Changes**

#### 1. **Configuration** (ackend/open_webui/config.py)
- Added RAG output format settings
- 5 predefined templates for different output styles
- Environment variable support for customization

#### 2. **Database Models**
- **Chat Model** (ackend/open_webui/models/chats.py)
  - Added params field for chat-specific RAG settings
  - New method update_chat_params_by_id()
- **User Model** (ackend/open_webui/models/users.py)
  - Added ag field in user settings

#### 3. **API Endpoints**
- **Chats Router** (ackend/open_webui/routers/chats.py)
  - POST /api/v1/chats/{id}/rag-params - Update chat RAG settings
- **Retrieval Router** (ackend/open_webui/routers/retrieval.py)
  - GET /api/v1/retrieval/output-formats - Get available formats

#### 4. **Utilities** (ackend/open_webui/utils/rag_utils.py)
- get_rag_output_format() - Determine format with priority system
- get_rag_template_by_format() - Get template for specific format
- pply_rag_format_settings() - Apply format-specific settings

#### 5. **Core Logic Updates**
- **Task Utils** (ackend/open_webui/utils/task.py)
  - Updated ag_template() function for format support
- **Middleware** (ackend/open_webui/utils/middleware.py)
  - Integrated RAG format selection in chat completion
- **Main App** (ackend/open_webui/main.py)
  - Added chat params to metadata

#### 6. **Database Migration**
- **Migration File** (ackend/open_webui/migrations/versions/add_chat_params_field.py)
  - Adds params JSON field to chat table

## How to Apply This Patch

### **Option 1: Manual File Replacement**
1. Copy each modified file to your Open WebUI installation
2. Run database migration: lembic upgrade head
3. Restart the application

### **Option 2: Copy and Merge**
1. Copy the modified files to your Open WebUI installation
2. Manually merge any conflicts if they exist
3. Run database migration

## Configuration

### **Environment Variables**
`ash
# Default output format
RAG_OUTPUT_FORMAT_DEFAULT=detailed

# Available formats
RAG_OUTPUT_FORMATS=compact,detailed,academic,table,list
`

## Priority System

1. **Per-Chat** (highest priority) - Chat-specific settings
2. **Per-User** - User's default preferences
3. **Global** (lowest priority) - System-wide defaults

## Testing

1. **Set user default format** in user settings
2. **Create new chat** and verify format is applied
3. **Override format** in specific chat
4. **Verify priority system** works correctly

## Original Repository

- **Open WebUI**: https://github.com/open-webui/open-webui
- **Author**: [Your Name]
- **Created**: [Date]
