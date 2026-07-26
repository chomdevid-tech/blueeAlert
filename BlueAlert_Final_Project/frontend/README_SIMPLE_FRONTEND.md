# BlueAlert Simple Flutter Frontend

This version uses only beginner-friendly concepts:

- Dart OOP
- StatelessWidget
- StatefulWidget
- setState
- callbacks
- async and await
- Firebase CRUD
- StreamBuilder
- MaterialPageRoute

It does not use Provider, ChangeNotifier, Bloc, Riverpod, or GetX.

## 1. Open the Flutter project

```powershell
cd "D:\CADT\Year 2 - term3\Mobile\final_project\bluealert_project\mobile_app"
```

When `pubspec.yaml` does not exist:

```powershell
flutter create --org com.chomdevid --project-name bluealert .
```

## 2. Add Firebase packages

```powershell
flutter pub add firebase_core
flutter pub add firebase_database
```

## 3. Generate Firebase configuration

```powershell
dart pub global activate flutterfire_cli
flutterfire configure
```

Choose the same Firebase project used by the Python backend.

This generates:

```text
lib/firebase_options.dart
```

Do not create that file manually.

## 4. Copy the code

Copy the provided `lib` and `test` folders into `mobile_app`.

## 5. Realtime Database development rules

Copy the content from:

```text
firebase/database.rules.json
```

Paste it into:

```text
Firebase Console
→ Realtime Database
→ Rules
```

Publish the rules.

These rules are only for a classroom demonstration without authentication.
They allow reading alerts and updating only the `status` field.

## 6. Format, analyze, and test

```powershell
dart format lib test
flutter analyze
flutter test
```

## 7. Run frontend

```powershell
flutter run -d chrome
```

## 8. Run backend in another PowerShell

```powershell
cd "D:\CADT\Year 2 - term3\Mobile\final_project\bluealert_project"

.\backend\.venv\Scripts\Activate.ps1

python -m backend.main
```

## Firebase structure

```text
alerts/{alertId}
```

Each alert must contain:

```text
alertId
title
description
attackType
severity
status
vmName
sourceIp
destinationIp
timestamp
rawLog
```
