# License Migration Summary: MIT to GNU GPL v3.0

## Overview
The LLB (爱学伴) project has been migrated from the MIT License to the GNU General Public License version 3.0 (GPL v3). This change affects all aspects of the project including source code, documentation, and contribution terms.

## Files Updated

### Core License Files
- ✅ `LICENSE` - Updated with complete GNU GPL v3.0 text
- ✅ `README.md` - Updated license badge and license section
- ✅ `CHANGELOG.md` - Added license change entry

### Documentation Files
- ✅ `CONTRIBUTING.md` - Updated contribution license terms from MIT to GPL v3
- ✅ `ai/datasets/README.md` - Updated license section to reflect GPL v3

### Configuration Files
- ✅ `frontend/package.json` - Added GPL-3.0 license field

### New Files Created
- ✅ `LICENSE_HEADER.txt` - Template for JavaScript/TypeScript/CSS files
- ✅ `LICENSE_HEADER_PYTHON.txt` - Template for Python files
- ✅ `LICENSE_MIGRATION_SUMMARY.md` - This summary document

## Key Changes Made

### 1. License Badge Update
**Before:**
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

**After:**
```markdown
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
```

### 2. License Section Update
**Before:**
```markdown
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

**After:**
```markdown
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for details.
```

### 3. Contribution Terms Update
**Before:**
```markdown
By contributing to LLB, you agree that your contributions will be licensed under the MIT License.
```

**After:**
```markdown
By contributing to LLB, you agree that your contributions will be licensed under the GNU General Public License v3.0.
```

## License Header Templates

### For JavaScript/TypeScript/CSS Files
Use the template in `LICENSE_HEADER.txt`:
```javascript
/*
 * LLB (爱学伴) - Local AI-Driven Sexual Health Education
 * Copyright (C) 2024 LLB Project Contributors
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
```

### For Python Files
Use the template in `LICENSE_HEADER_PYTHON.txt`:
```python
# LLB (爱学伴) - Local AI-Driven Sexual Health Education
# Copyright (C) 2024 LLB Project Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

## Impact of GPL v3 License

### What This Means for Users
- ✅ You can still use the software freely
- ✅ You can modify the software
- ✅ You can distribute the software
- ⚠️ Any modifications must also be licensed under GPL v3
- ⚠️ Source code must be made available when distributing

### What This Means for Contributors
- ✅ Your contributions help ensure the software remains free
- ✅ Your contributions are protected by copyleft
- ⚠️ All contributions must be compatible with GPL v3
- ⚠️ You cannot contribute proprietary code

### What This Means for Commercial Use
- ✅ Commercial use is allowed
- ✅ You can charge for the software
- ⚠️ You must provide source code to customers
- ⚠️ Any modifications must be licensed under GPL v3
- ⚠️ Cannot be incorporated into proprietary software

## Compliance Requirements

### For Distributors
1. Include a copy of the GPL v3 license
2. Provide source code or offer to provide it
3. Preserve all copyright notices
4. Include installation information for user products

### For Developers
1. Add license headers to new source files
2. Ensure all dependencies are GPL-compatible
3. Document any changes made to the software
4. Maintain the GPL v3 license for derivative works

## Next Steps

### For New Source Files
- Add appropriate license headers using the templates provided
- Ensure all new code is compatible with GPL v3

### For Existing Source Files
- Gradually add license headers to existing files
- Review and update any files that may have conflicting licenses

### For Dependencies
- Review all project dependencies for GPL compatibility
- Replace any incompatible dependencies

## Resources

- [GNU GPL v3 Full Text](https://www.gnu.org/licenses/gpl-3.0.html)
- [GPL v3 Quick Guide](https://www.gnu.org/licenses/quick-guide-gplv3.html)
- [GPL Compatibility Matrix](https://www.gnu.org/licenses/license-compatibility.html)
- [How to Apply GPL to Your Programs](https://www.gnu.org/licenses/gpl-howto.html)

## Questions or Concerns

If you have questions about this license change or its implications:
- Review the [GNU GPL v3 FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- Open an issue in the project repository
- Contact the project maintainers

---

**Date of Migration:** December 2024  
**Migration Completed By:** Project Maintainers  
**Review Status:** ✅ Complete 