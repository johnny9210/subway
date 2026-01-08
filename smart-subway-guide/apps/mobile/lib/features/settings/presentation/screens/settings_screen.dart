import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('설정'),
      ),
      body: ListView(
        children: [
          const _SettingsSection(title: '일반'),
          ListTile(
            leading: const Icon(Icons.directions_subway),
            title: const Text('자주 가는 방향'),
            subtitle: const Text('자주 이용하는 방향을 설정합니다'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              // TODO: 자주 가는 방향 설정
            },
          ),
          const Divider(),
          const _SettingsSection(title: '데이터'),
          SwitchListTile(
            secondary: const Icon(Icons.cloud_upload),
            title: const Text('데이터 수집 참여'),
            subtitle: const Text('익명화된 이동 시간 데이터를 제공합니다'),
            value: true,
            onChanged: (value) {
              // TODO: 데이터 수집 토글
            },
          ),
          const Divider(),
          const _SettingsSection(title: '앱 정보'),
          ListTile(
            leading: const Icon(Icons.info_outline),
            title: const Text('버전'),
            subtitle: const Text('1.0.0'),
          ),
          ListTile(
            leading: const Icon(Icons.description),
            title: const Text('개인정보 처리방침'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              // TODO: 개인정보 처리방침
            },
          ),
          ListTile(
            leading: const Icon(Icons.article),
            title: const Text('이용약관'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              // TODO: 이용약관
            },
          ),
        ],
      ),
    );
  }
}

class _SettingsSection extends StatelessWidget {
  final String title;

  const _SettingsSection({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.w600,
          color: Theme.of(context).colorScheme.primary,
        ),
      ),
    );
  }
}
