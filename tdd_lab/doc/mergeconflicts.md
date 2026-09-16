**IMPORTANT: How to Handle Merge Conflicts in the Testing Lab** 

Hey everyone! Since multiple students are modifying `counter.py` in the **Testing Lab**, merge conflicts **will likely occur** when merging Pull Requests (PRs). This is a normal part of software development, and resolving conflicts is a valuable skill.  

Follow these steps to **avoid and resolve merge conflicts smoothly**:  

---

## ✅ **Best Practices to Avoid Conflicts**
### **1 Before working on your branch, always pull the latest changes**
```bash
git checkout main
git pull origin main
git checkout -b add-method-<your-method>
```
### **Commit and push frequently to reduce the chances of conflicts.**
### **Before submitting your PR, always pull the latest changes from main and merge them into your branch:**
```bash
git checkout main
git pull origin main
git checkout add-method-<your-method>
git merge main  # Merges the latest changes from main
```
- If there are conflicts, Git will notify you.

## **Resolving Merge Conflicts in counter.py**
If a conflict occurs, Git will mark the conflicting lines in `counter.py` like this:

```python
def create_counter(name):
<<<<<<< HEAD
    """Create a counter (Student A's version)"""
    if name in COUNTERS:
        return jsonify({"error": "Counter already exists"}), 409
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), 201
=======
    """Creates a counter if not exists (Student B's version)"""
    if name not in COUNTERS:
        COUNTERS[name] = 0
        return jsonify({name: COUNTERS[name]}), 201
    return jsonify({"error": "Counter already exists"}), 409
>>>>>>> add-method-create-counter
```

### 🛠️ **How to fix it manually:**
- Decide which version to keep (or merge both logically).
- Remove Git conflict markers (`<<<<<<<, =======, >>>>>>>`).
- Ensure the final function is correct and consistent.

Example fixed version:
```python
def create_counter(name):
    """Create a counter if it does not exist"""
    if name not in COUNTERS:
        COUNTERS[name] = 0
        return jsonify({name: COUNTERS[name]}), 201
    return jsonify({"error": "Counter already exists"}), 409
```

## **Finalizing the Merge**
```bash
git add counter.py  # Stage the fixed file
git commit -m "Resolved merge conflict in counter.py"
git push origin add-method-<your-method>
```

## 🛠️ **Too Long; Didn't Read**
✅ **Before you start** → `git pull origin main`  
✅ **Before pushing your PR** → `git pull origin main && git merge main`  
✅ **If you see a conflict** → Edit the file, remove conflict markers, commit the fix  
✅ **Push the resolved changes** → `git push origin <your-branch>`