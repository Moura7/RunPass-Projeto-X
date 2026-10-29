import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'identity_gateway.dart';

typedef PhotoSelector = Future<List<int>?> Function();

String displayDate(String value) {
  final parts = value.split('-');
  return parts.length == 3 ? '${parts[2]}/${parts[1]}/${parts[0]}' : value;
}

String catalogError(IdentityIssue issue) => switch (issue.code) {
  'INVALID_TOKEN' || 'ACCOUNT_UNAVAILABLE' =>
    'Sua sessão não está disponível. Volte e entre novamente.',
  'BETA_ADMISSION_REQUIRED' =>
    'É necessário participar do beta para consultar as corridas.',
  'INVALID_CURSOR' =>
    'A busca expirou. Toque em Buscar para começar novamente.',
  'INVALID_INPUT' ||
  'INVALID_FILTERS' => 'Confira os filtros, as datas e a distância informada.',
  'EDITION_NOT_FOUND' => 'Esta edição não está disponível.',
  'EDITION_ARCHIVED' ||
  'EDITION_CHANGED' => 'Esta edição mudou e não aceita um novo rascunho.',
  'DISTANCE_NOT_IN_EDITION' => 'A distância não pertence mais a esta edição.',
  'PARTICIPATION_EXISTS' => 'Você já possui um registro para esta edição.',
  'VERSION_CONFLICT' =>
    'O rascunho mudou em outro lugar. Reabra-o antes de editar.',
  'IMAGE_SIZE_INVALID' => 'A foto deve ter no máximo 10 MB.',
  'IMAGE_FORMAT_INVALID' =>
    'Escolha uma foto JPEG ou PNG. Não foi possível converter esta imagem.',
  'INVALID_IMAGE' || 'FORMAT_MISMATCH' || 'PIXEL_LIMIT_EXCEEDED' =>
    'A foto não pôde ser validada. O rascunho foi preservado.',
  'PROCESSING_TIMEOUT' || 'UPLOAD_UNAVAILABLE' =>
    'A foto não foi processada. Tente novamente; o rascunho foi preservado.',
  'IMAGE_NOT_VALID' => 'A imagem não está válida. O rascunho foi preservado.',
  'EDITION_NOT_COMPLETABLE' => 'Esta corrida ainda não pode ser concluída.',
  'PARTICIPATION_NOT_DRAFT' =>
    'Esta participação já foi concluída ou alterada.',
  _ => 'Não foi possível carregar as corridas. Tente novamente.',
};

class CatalogScreen extends StatefulWidget {
  final IdentityGateway gateway;
  const CatalogScreen({super.key, required this.gateway});
  @override
  State<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends State<CatalogScreen> {
  final fields = {
    for (final key in [
      'namePrefix',
      'city',
      'state',
      'distanceKm',
      'dateFrom',
      'dateTo',
    ])
      key: TextEditingController(),
  };
  final form = GlobalKey<FormState>();
  final items = <Map<String, dynamic>>[];
  Map<String, String> activeFilters = {};
  String? nextCursor, error;
  bool loading = false;

  @override
  void initState() {
    super.initState();
    load();
  }

  @override
  void dispose() {
    for (final controller in fields.values) {
      controller.dispose();
    }
    super.dispose();
  }

  Future<void> load({bool more = false}) async {
    if (loading) return;
    if (!more && !(form.currentState?.validate() ?? true)) return;
    if (!more) {
      activeFilters = {
        for (final entry in fields.entries)
          if (entry.value.text.trim().isNotEmpty)
            entry.key: entry.value.text.trim(),
      };
      items.clear();
      nextCursor = null;
    }
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final page = await widget.gateway.request(
        '/editions',
        query: {
          ...activeFilters,
          'limit': '20',
          if (more && nextCursor != null) 'cursor': nextCursor!,
        },
      );
      if (!mounted) return;
      final known = items.map((e) => e['id']).toSet();
      for (final entry
          in (page['items'] as List).cast<Map<String, dynamic>>()) {
        if (known.add(entry['id'])) items.add(entry);
      }
      nextCursor = page['nextCursor'] as String?;
    } on IdentityIssue catch (issue) {
      if (mounted) error = catalogError(issue);
    } on Exception {
      if (mounted) error = 'Não foi possível conectar. Tente novamente.';
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Widget filter(
    String key,
    String label, {
    String? Function(String)? validate,
    int? maxLength,
  }) => Padding(
    padding: const EdgeInsets.only(bottom: 8),
    child: TextFormField(
      controller: fields[key],
      maxLength: maxLength,
      decoration: InputDecoration(labelText: label),
      keyboardType: key == 'distanceKm'
          ? const TextInputType.numberWithOptions(decimal: true)
          : TextInputType.text,
      validator: (value) => value == null || value.trim().isEmpty
          ? null
          : validate?.call(value.trim()),
    ),
  );

  String? dateValidator(String value) {
    final parsed = DateTime.tryParse(value);
    if (!RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(value) ||
        parsed == null ||
        parsed.toIso8601String().substring(0, 10) != value) {
      return 'Use uma data válida no formato AAAA-MM-DD.';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Descobrir corridas')),
    body: SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Form(
            key: form,
            child: Column(
              children: [
                filter(
                  'namePrefix',
                  'Início do nome da corrida',
                  maxLength: 160,
                ),
                filter('city', 'Cidade', maxLength: 100),
                filter(
                  'state',
                  'Estado (UF)',
                  maxLength: 2,
                  validate: (value) => RegExp(r'^[A-Za-z]{2}$').hasMatch(value)
                      ? null
                      : 'Informe a UF.',
                ),
                filter(
                  'distanceKm',
                  'Distância em km',
                  validate: (value) {
                    final km = double.tryParse(value);
                    return km != null && km.isFinite && km > 0
                        ? null
                        : 'Informe uma distância positiva, usando ponto para decimais.';
                  },
                ),
                filter(
                  'dateFrom',
                  'Data inicial (AAAA-MM-DD)',
                  validate: dateValidator,
                ),
                filter(
                  'dateTo',
                  'Data final (AAAA-MM-DD)',
                  validate: dateValidator,
                ),
                FilledButton(
                  onPressed: loading ? null : () => load(),
                  child: const Text('Buscar'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          if (error != null) ...[
            Text(error!, key: const Key('catalog-error')),
            TextButton(
              onPressed: loading ? null : () => load(more: nextCursor != null),
              child: const Text('Tentar novamente'),
            ),
          ],
          if (loading) const Center(child: CircularProgressIndicator()),
          if (!loading && error == null && items.isEmpty)
            Text(
              nextCursor == null
                  ? 'Nenhuma corrida encontrada com esses filtros.'
                  : 'Nenhuma corrida nesta página. Continue a busca.',
            ),
          for (final edition in items)
            Card(
              child: ListTile(
                title: Text(edition['name'] as String),
                subtitle: Text(
                  '${displayDate(edition['date'] as String)} · ${edition['city']}/${edition['state']}\n'
                  '${(edition['distances'] as List).map((d) => '${d['kilometers']} km').join(' · ')}'
                  '${edition['status'] == 'archived' ? '\nEdição arquivada' : ''}',
                ),
                isThreeLine: true,
                onTap: loading
                    ? null
                    : () => Navigator.of(context).push(
                        MaterialPageRoute<void>(
                          builder: (_) => EditionScreen(
                            gateway: widget.gateway,
                            editionId: edition['id'] as String,
                          ),
                        ),
                      ),
              ),
            ),
          if (nextCursor != null)
            TextButton(
              onPressed: loading ? null : () => load(more: true),
              child: const Text('Carregar mais'),
            ),
        ],
      ),
    ),
  );
}

class EditionScreen extends StatefulWidget {
  final IdentityGateway gateway;
  final String editionId;
  const EditionScreen({
    super.key,
    required this.gateway,
    required this.editionId,
  });
  @override
  State<EditionScreen> createState() => _EditionScreenState();
}

class _EditionScreenState extends State<EditionScreen> {
  Map<String, dynamic>? edition;
  String? selectedDistance, error;
  bool loading = true, saving = false;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final result = await widget.gateway.request(
        '/editions/${Uri.encodeComponent(widget.editionId)}',
      );
      if (mounted) edition = result;
    } on IdentityIssue catch (issue) {
      if (mounted) error = catalogError(issue);
    } on Exception {
      if (mounted) error = 'Não foi possível conectar. Tente novamente.';
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final body = edition;
    return Scaffold(
      appBar: AppBar(title: const Text('Detalhes da edição')),
      body: SafeArea(
        child: loading
            ? const Center(child: CircularProgressIndicator())
            : error != null
            ? Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(error!),
                    TextButton(
                      onPressed: load,
                      child: const Text('Tentar novamente'),
                    ),
                  ],
                ),
              )
            : body == null
            ? const SizedBox.shrink()
            : ListView(
                padding: const EdgeInsets.all(24),
                children: [
                  Text(
                    body['name'] as String,
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    '${displayDate(body['date'] as String)} · ${body['city']}/${body['state']}',
                  ),
                  if (body['description'] != null)
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      child: Text(body['description'] as String),
                    ),
                  if (body['organizerName'] != null)
                    Text('Organização: ${body['organizerName']}'),
                  if (body['status'] == 'archived')
                    const Text(
                      'Edição arquivada: o histórico está preservado e novos registros não estão disponíveis.',
                    ),
                  const SizedBox(height: 16),
                  const Text('Distâncias'),
                  for (final distance in body['distances'] as List)
                    ListTile(
                      title: Text('${distance['kilometers']} km'),
                      leading: Icon(
                        selectedDistance == distance['id']
                            ? Icons.radio_button_checked
                            : Icons.radio_button_unchecked,
                      ),
                      selected: selectedDistance == distance['id'],
                      subtitle:
                          distance['medalImageReference'] != null ||
                              body['medalImageReference'] != null
                          ? const Text('Imagem oficial da medalha disponível')
                          : null,
                      onTap: body['status'] == 'archived'
                          ? null
                          : () => setState(
                              () => selectedDistance = distance['id'] as String,
                            ),
                    ),
                  if (selectedDistance != null)
                    const Text('Distância selecionada.'),
                  if (selectedDistance != null) ...[
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: saving
                          ? null
                          : () async {
                              setState(() {
                                saving = true;
                                error = null;
                              });
                              try {
                                final draft = await widget.gateway.request(
                                  '/participations',
                                  method: 'POST',
                                  body: {
                                    'editionId': widget.editionId,
                                    'distanceId': selectedDistance,
                                  },
                                );
                                if (!context.mounted) return;
                                await Navigator.of(context).push(
                                  MaterialPageRoute<void>(
                                    builder: (_) => ParticipationDraftScreen(
                                      gateway: widget.gateway,
                                      initial: draft,
                                    ),
                                  ),
                                );
                              } on IdentityIssue catch (issue) {
                                if (mounted) error = catalogError(issue);
                              } finally {
                                if (mounted) setState(() => saving = false);
                              }
                            },
                      child: Text(saving ? 'Salvando...' : 'Criar rascunho'),
                    ),
                  ],
                ],
              ),
      ),
    );
  }
}

class ParticipationDraftScreen extends StatefulWidget {
  final IdentityGateway gateway;
  final Map<String, dynamic> initial;
  final PhotoSelector? photoSelector;
  const ParticipationDraftScreen({
    super.key,
    required this.gateway,
    required this.initial,
    this.photoSelector,
  });

  @override
  State<ParticipationDraftScreen> createState() =>
      _ParticipationDraftScreenState();
}

class _ParticipationDraftScreenState extends State<ParticipationDraftScreen> {
  late Map<String, dynamic> draft;
  late final TextEditingController time, placement, bib;
  late final TextEditingController comment;
  String? message;
  bool saving = false, uploading = false;
  String? imageReference, pendingUploadId;
  bool declaredCompleted = false, publishToFeed = false;
  final ratings = {
    'organization': 5,
    'course': 5,
    'kit': 5,
    'medal': 5,
    'hydration': 5,
    'facilities': 5,
    'safety': 5,
    'valueForMoney': 5,
  };
  static const ratingLabels = {
    'organization': 'Organização',
    'course': 'Percurso',
    'kit': 'Kit',
    'medal': 'Medalha',
    'hydration': 'Hidratação',
    'facilities': 'Estrutura',
    'safety': 'Segurança',
    'valueForMoney': 'Custo-benefício',
  };

  @override
  void initState() {
    super.initState();
    draft = Map<String, dynamic>.from(widget.initial);
    time = TextEditingController(text: draft['timeSeconds']?.toString() ?? '');
    placement = TextEditingController(
      text: draft['placement']?.toString() ?? '',
    );
    bib = TextEditingController(text: draft['bibNumber'] as String? ?? '');
    comment = TextEditingController();
  }

  @override
  void dispose() {
    time.dispose();
    placement.dispose();
    bib.dispose();
    comment.dispose();
    super.dispose();
  }

  int? positive(String value) {
    if (value.trim().isEmpty) return null;
    final parsed = int.tryParse(value);
    return parsed != null && parsed > 0 ? parsed : -1;
  }

  Future<void> save() async {
    final seconds = positive(time.text), place = positive(placement.text);
    if (seconds == -1 || place == -1 || bib.text.length > 40) {
      setState(() => message = 'Confira tempo, colocação e número de peito.');
      return;
    }
    setState(() {
      saving = true;
      message = null;
    });
    try {
      draft = await widget.gateway.request(
        '/participations/${Uri.encodeComponent(draft['id'] as String)}',
        method: 'PATCH',
        body: {
          'expectedVersion': draft['version'],
          'timeSeconds': seconds,
          'placement': place,
          'bibNumber': bib.text.trim().isEmpty ? null : bib.text.trim(),
        },
      );
      if (mounted) message = 'Rascunho salvo. Nada foi publicado.';
    } on IdentityIssue catch (issue) {
      if (mounted) message = catalogError(issue);
    } finally {
      if (mounted) setState(() => saving = false);
    }
  }

  Future<void> selectPhoto() async {
    setState(() {
      uploading = true;
      message = null;
    });
    try {
      List<int>? bytes;
      if (widget.photoSelector != null) {
        bytes = await widget.photoSelector!();
      } else {
        final file = await ImagePicker().pickImage(
          source: ImageSource.gallery,
          maxWidth: 5000,
          maxHeight: 5000,
          imageQuality: 85,
          requestFullMetadata: false,
        );
        bytes = await file?.readAsBytes();
      }
      if (bytes == null) return;
      final contentType =
          bytes.length >= 3 &&
              bytes[0] == 0xff &&
              bytes[1] == 0xd8 &&
              bytes[2] == 0xff
          ? 'image/jpeg'
          : bytes.length >= 8 &&
                bytes[0] == 0x89 &&
                bytes[1] == 0x50 &&
                bytes[2] == 0x4e &&
                bytes[3] == 0x47
          ? 'image/png'
          : null;
      if (contentType == null) {
        throw const IdentityIssue('IMAGE_FORMAT_INVALID');
      }
      final result = await widget.gateway.uploadImage(bytes, contentType);
      if (result['state'] == 'valid') {
        imageReference = result['imageReference'] as String;
        pendingUploadId = null;
        message = 'Foto validada e privada. Ainda não foi publicada.';
      } else if (result['state'] == 'failed') {
        throw IdentityIssue(result['reasonCode'] as String? ?? 'INVALID_IMAGE');
      } else {
        pendingUploadId = result['uploadId'] as String;
        message = 'Foto recebida e ainda em processamento.';
      }
    } on IdentityIssue catch (issue) {
      if (mounted) message = catalogError(issue);
    } on Exception {
      if (mounted) {
        message =
            'Não foi possível selecionar a foto. O rascunho foi preservado.';
      }
    } finally {
      if (mounted) setState(() => uploading = false);
    }
  }

  Future<void> refreshPhoto() async {
    final uploadId = pendingUploadId;
    if (uploadId == null) return;
    setState(() {
      uploading = true;
      message = null;
    });
    try {
      final result = await widget.gateway.uploadStatus(uploadId);
      if (result['state'] == 'valid') {
        imageReference = result['imageReference'] as String;
        pendingUploadId = null;
        message = 'Foto validada e privada. Ainda não foi publicada.';
      } else if (result['state'] == 'failed') {
        pendingUploadId = null;
        throw IdentityIssue(result['reasonCode'] as String? ?? 'INVALID_IMAGE');
      } else {
        message =
            'A foto continua em processamento. Tente consultar novamente.';
      }
    } on IdentityIssue catch (issue) {
      if (mounted) message = catalogError(issue);
    } finally {
      if (mounted) setState(() => uploading = false);
    }
  }

  Future<void> complete() async {
    if (imageReference == null || !declaredCompleted) {
      setState(
        () => message = 'Confirme a conclusão e use uma imagem validada.',
      );
      return;
    }
    setState(() {
      saving = true;
      message = null;
    });
    try {
      draft = await widget.gateway.request(
        '/participations/${Uri.encodeComponent(draft['id'] as String)}/complete',
        method: 'POST',
        body: {
          'expectedVersion': draft['version'],
          'declaredCompleted': true,
          'ratings': ratings,
          'medalImageReference': imageReference,
          'publishToFeed': publishToFeed,
          if (comment.text.isNotEmpty) 'comment': comment.text,
        },
      );
      if (mounted) {
        message = 'Participação concluída. Avaliação e medalha foram salvas.';
      }
    } on IdentityIssue catch (issue) {
      if (mounted) message = catalogError(issue);
    } finally {
      if (mounted) setState(() => saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (draft['state'] == 'completed') {
      return Scaffold(
        appBar: AppBar(title: const Text('Participação concluída')),
        body: const Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.emoji_events_outlined, size: 48),
              SizedBox(height: 16),
              Text('Participação concluída · medalha e avaliação registradas.'),
              SizedBox(height: 8),
              Text(
                'A conquista permanece privada enquanto a publicação não estiver disponível.',
              ),
            ],
          ),
        ),
      );
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Rascunho da participação')),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          const Text('Privado · não gera medalha, avaliação ou publicação.'),
          TextField(
            controller: time,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Tempo em segundos (opcional)',
            ),
          ),
          TextField(
            controller: placement,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Colocação (opcional)',
            ),
          ),
          TextField(
            controller: bib,
            maxLength: 40,
            decoration: const InputDecoration(
              labelText: 'Número de peito (opcional)',
            ),
          ),
          FilledButton(
            onPressed: saving ? null : save,
            child: Text(saving ? 'Salvando...' : 'Salvar rascunho'),
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            onPressed: saving || uploading ? null : selectPhoto,
            icon: const Icon(Icons.photo_library_outlined),
            label: Text(uploading ? 'Enviando foto...' : 'Selecionar foto'),
          ),
          if (imageReference != null)
            const Text('Imagem validada para uso na conclusão.'),
          if (pendingUploadId != null)
            TextButton(
              onPressed: uploading ? null : refreshPhoto,
              child: const Text('Consultar processamento da foto'),
            ),
          if (imageReference != null && draft['state'] == 'draft') ...[
            const Divider(height: 32),
            const Text('Avaliação obrigatória'),
            for (final entry in ratingLabels.entries)
              DropdownButtonFormField<int>(
                initialValue: ratings[entry.key],
                decoration: InputDecoration(labelText: entry.value),
                items: [1, 2, 3, 4, 5]
                    .map(
                      (value) =>
                          DropdownMenuItem(value: value, child: Text('$value')),
                    )
                    .toList(),
                onChanged: (value) {
                  if (value != null) ratings[entry.key] = value;
                },
              ),
            TextField(
              controller: comment,
              maxLength: 2000,
              decoration: const InputDecoration(
                labelText: 'Comentário (opcional)',
              ),
            ),
            CheckboxListTile(
              value: declaredCompleted,
              onChanged: (value) =>
                  setState(() => declaredCompleted = value ?? false),
              title: const Text('Declaro que concluí esta corrida'),
            ),
            CheckboxListTile(
              value: publishToFeed,
              onChanged: (value) =>
                  setState(() => publishToFeed = value ?? false),
              title: const Text(
                'Publicar conquista quando o feed estiver disponível',
              ),
            ),
            FilledButton(
              onPressed: saving ? null : complete,
              child: Text(saving ? 'Concluindo...' : 'Concluir participação'),
            ),
          ],
          if (message != null) Text(message!, key: const Key('draft-message')),
        ],
      ),
    );
  }
}
